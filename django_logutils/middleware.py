# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


class LoggingMiddleware(object):
    """Capture request info and logs it.

    Logs all requests to info. If request take longer than MAX_WARNING_TIME,
    info is logged to warning.

    Simple logging middleware that captures the following:
        * remote address (whether proxied or direct).
        * if authenticated, then user email address.
        * request method (GET/POST etc).
        * request full path.
        * response status code (200, 404 etc).
        * content length.
        * request process time.
        * If DEBUG=True or MAX_WARNING_TIME is exceeded, also logs SQL query
            information - number of queries and how long they too.

    Based on: https://djangosnippets.org/snippets/2624/
    """

    def process_request(self, request):
        """Add start time to request.
        """
        self.start_time = time.time()

    def process_response(self, request, response):
        """Get info from request and send to response.
        """

        MAX_WARNING_TIME = 1.

        try:
            remote_addr = request.META.get('REMOTE_ADDR')
            if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get(
                    'HTTP_X_FORWARDED_FOR') or remote_addr
            user_email = "-"
            extra_log = {'nr_queries': 0, 'sql_time': 0}
            if hasattr(request, 'user'):
                user_email = getattr(request.user, 'email', '-')
            # Fix 'LoggingMiddleware' object has no attribute 'start_time'.
            # The process_response() method cannot rely on setup done in
            # process_request().
            req_time = (time.time() - self.start_time
                        if hasattr(self, 'start_time') else .0)
            content_len = len(response.content)

            log_dict = {
                # 'event' makes event-based filtering possible in logging
                # backends like logstash
                'event': 'request_response',
                'remote_address': remote_addr,
                'user_email': user_email,
                'method': request.method,
                'url': request.get_full_path(),
                'status': response.status_code,
                'content_length': content_len,
                'request_time': req_time,
            }

            log_msg = ("{remote_address} {user_email} {method} {url} {status}"
                       " {content_length} ({request_time:.2f} seconds)")

            if settings.DEBUG or req_time > MAX_WARNING_TIME:
                sql_time = sum(
                    float(q['time']) for q in connection.queries) * 1000
                extra_log = {'nr_queries': len(connection.queries),
                             'sql_time': sql_time}
                log_msg += " ({nr_queries} SQL queries, {sql_time} ms)"
                log_dict.update(extra_log)

            log_msg = log_msg.format(**log_dict)

            if req_time > MAX_WARNING_TIME:
                logger.warning(log_msg, extra=log_dict)
            else:
                logger.info(log_msg, extra=log_dict)

        except Exception as e:
            logger.exception(e)

        return response
