# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from django.conf import settings
from django.db import connection

from django_logutils.models import LogutilsAppConf

appsettings = LogutilsAppConf()

logger = logging.getLogger(__name__)


def create_log_dict(request, response):
    """
    Create a dictionary with logging data.
    """
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
        remote_addr = request.META.get(
            'HTTP_X_FORWARDED_FOR') or remote_addr

    user_email = "-"
    if hasattr(request, 'user'):
        user_email = getattr(request.user, 'email', '-')

    return {
        # 'event' makes event-based filtering possible in logging backends
        # like logstash
        'event': appsettings.LOGGING_MIDDLEWARE_EVENT,
        'remote_address': remote_addr,
        'user_email': user_email,
        'method': request.method,
        'url': request.get_full_path(),
        'status': response.status_code,
        'content_length': len(response.content),
        'request_time': -1,  # NA value: real value added by LoggingMiddleware
    }


def create_log_message(log_dict, use_sql_info=False):
    """
    Create the logging message string.
    """
    log_msg = (
        "{remote_address} {user_email} {method} {url} {status} "
        "{content_length} ({request_time:.2f} seconds)"
    )
    if use_sql_info:
        sql_time = sum(
            float(q['time']) for q in connection.queries) * 1000
        extra_log = {
            'nr_queries': len(connection.queries),
            'sql_time': sql_time}
        log_msg += " ({nr_queries} SQL queries, {sql_time} ms)"
        log_dict.update(extra_log)
    return log_msg.format(**log_dict)


class LoggingMiddleware(object):
    """
    Capture request info and logs it.

    Logs all requests with log level info. If request take longer than
    REQUEST_TIME_THRESHOLD, log level warningis used.

    Logging middleware that captures the following:
        * logging event.
        * remote address (whether proxied or direct).
        * if authenticated, then user email address.
        * request method (GET/POST etc).
        * request full path.
        * response status code (200, 404 etc).
        * content length.
        * request process time.
        * if DEBUG=True or REQUEST_TIME_THRESHOLD is exceeded, also logs SQL
          query information - number of queries and how long they too.

    Based on: https://djangosnippets.org/snippets/2624/

    """
    def __init__(self, *args, **kwargs):
        """
        Add initial empty start_time.
        """
        self.start_time = None

    def process_request(self, request):
        """
        Add start time to request.
        """
        self.start_time = time.time()

    def process_response(self, request, response):
        """
        Create the logging message..
        """
        REQUEST_TIME_THRESHOLD = 1.

        try:
            log_dict = create_log_dict(request, response)

            # add the request time to the log_dict; if no start time is
            # available, use -1 as NA value
            request_time = (
                time.time() - self.start_time if hasattr(self, 'start_time')
                and self.start_time else -1)
            log_dict.update({'request_time': request_time})

            is_request_time_too_high = request_time > REQUEST_TIME_THRESHOLD
            use_sql_info = settings.DEBUG or is_request_time_too_high

            log_msg = create_log_message(log_dict, use_sql_info)

            if is_request_time_too_high:
                logger.warning(log_msg, extra=log_dict)
            else:
                logger.info(log_msg, extra=log_dict)
        except Exception as e:
            logger.exception(e)

        return response
