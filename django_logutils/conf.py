# -*- coding: utf-8 -*-
from django.conf import settings  # noqa
from appconf import AppConf


class LogutilsAppConf(AppConf):
    LOGGING_MIDDLEWARE_EVENT = 'request'
    REQUEST_TIME_THRESHOLD = 1.

    class Meta:
        prefix = 'logutils'
