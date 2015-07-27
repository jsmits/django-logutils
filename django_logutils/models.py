# -*- coding: utf-8 -*-
from appconf import AppConf


class LogutilsAppConf(AppConf):
    LOGGING_MIDDLEWARE_EVENT = 'request'

    class Meta:
        prefix = 'logutils'
