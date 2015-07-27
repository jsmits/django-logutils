import time

from django.http import HttpRequest, HttpResponse

from django_logutils import middleware


def test_log_dict():
    request = HttpRequest()
    response = HttpResponse()
    log_dict = middleware.create_log_dict(request, response)
    assert len(log_dict) == 8

def test_empty_log_message():
    request = HttpRequest()
    response = HttpResponse()
    log_dict = middleware.create_log_dict(request, response)
    log_msg = middleware.create_log_message(log_dict)
    # assert that log_msg is an empty log message
    assert log_msg == 'None - None  200 0 (-1.00 seconds)'

def test_empty_logging_middleware_response():
    request = HttpRequest()
    response = HttpResponse()
    mw = middleware.LoggingMiddleware()
    mw.process_request(request)
    response = mw.process_response(request, response)
    assert response.status_code == 200
