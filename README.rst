=============================
django-logutils
=============================

.. image:: https://badge.fury.io/py/django-logutils.png
    :target: https://badge.fury.io/py/django-logutils

.. image:: https://travis-ci.org/jsmits/django-logutils.png?branch=master
    :target: https://travis-ci.org/jsmits/django-logutils

Various logging-related utilities for Django projects. For now, it provides
a LoggingMiddleware class.

Quickstart
----------

Install django-logutils::

    pip install django-logutils

LoggingMiddleware
-----------------

LoggingMiddleware is middleware class for Django, that logs extra
request-related information. To use it in your Django projects, add it to
your `MIDDLEWARE_CLASSES` setting::

    MIDDLEWARE_CLASSES = (
        ...
        'django_logutils.middleware.LoggingMiddleware',
        ...
    )

The extra information consists of:

- event (default: 'request', can be overridden by using the
  LOGUTILS_LOGGING_MIDDLEWARE_EVENT setting in your project

- remote ip address: the remote ip address of the user doing the request.

- user email: the email address of the requesting user, if available

- request method: post or get

- request url path

- response status code

- content length of the response body

- request time

The log message itself is a string composed of the remote ip address, the user
email, the request method, the request url, the status code, the content
length of the body and the request time. Additionally, a dictionary with the
log items are added as a extra keyword argument when sending a logging
statement.

If settings.DEBUG is True or the request time is more than 1 second, two
 additional parameters are added to the logging dictionary: `nr_queries` that
 represents the number of queries executed during the request-response cycle
 and `sql_time` that represents the time it took to execute those queries.

Development
-----------

Install the test requirements::

    $ pip install -r requirements/test.txt

Run the tests to check everything is fine::

    $ make test

To run the tests and opening the coverage html in your browser::

    $ make coverage

To run flake8 and pylint, do::

    $ make lint

To generate the documentation, do::

    $ make docs
