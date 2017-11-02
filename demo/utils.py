# coding=utf-8
ColorFormatter = None


def _patch_models_to_dict():
    """
    Add a `to_dict` method into every Model
    that inherit from `models.Model`
    """
    from itertools import chain
    from django.db import models
    # from django.contrib.contenttypes import fields

    # django.forms.models.model_to_dict
    def model_to_dict(instance, fields=None, exclude=None):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, 'editable', False):
            #     continue
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(instance)
        return data

    def to_dict(instance, *args, **kw):
        return models.Model._to_dict(instance, *args, **kw)

    models.Model._to_dict = model_to_dict
    models.Model.to_dict = to_dict


def _patch_windows_console_color():
    import platform
    from django.core.management import color
    try:
        from colorama import init
    except ImportError:
        pass
    else:
        if platform.system() == 'Windows':
            init()
            color.supports_color = lambda: True


def _patch_pymysql_as_mysqldb():
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass


def _patch_request_query_dict():
    from django.http.request import HttpRequest

    def get_query_dict(request):
        data = {}
        for key in request.GET.keys():
            data[key] = request.GET.getlist(key)
        for key in request.POST.keys():
            data[key] = request.POST.getlist(key)
        for key in data.keys():
            if data[key] is []:
                data[key] = ''
            elif len(data[key]) == 1:
                data[key] = data[key][0]
        return data
    HttpRequest.QueryDict = property(get_query_dict)


def _patch_logger(settings):
    import os
    import logging
    from django.core.management.color import color_style
    global ColorFormatter

    class ColorFormatter(logging.StreamHandler):

        def __init__(self, *args, **kwargs):
            self.style = color_style()
            setattr(self.style, 'DEBUG', self.style.SUCCESS)
            setattr(self.style, 'INFO', self.style.HTTP_INFO)
            setattr(self.style, 'MESSAGE', self.style.HTTP_NOT_MODIFIED)
            super(ColorFormatter, self).__init__(*args, **kwargs)

        def emit(self, record):
            colorize = getattr(self.style, record.levelname, None)
            if colorize:
                record.levelname = colorize(record.levelname)
            record.msg = self.style.MESSAGE(record.msg)
            return super(ColorFormatter, self).emit(record)

    setattr(settings, 'LOGGING', {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'costom': {
                'format': '\n%(levelname)s %(asctime)s@%(name)s.%(funcName)s:%(lineno)d %(message)s'
            },
            'console': {
                'format': '\n%(levelname)s %(asctime)s@%(name)s.%(funcName)s:%(lineno)d\n%(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'demo.utils.ColorFormatter',
                'formatter': 'console'
            },
            'debug': {
                'backupCount': 5,
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'filename': os.path.join(settings.LOG_PATH, 'debug.log'),
                'formatter': 'costom',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 5242880
            },
        },
        'loggers': {
            '': {
                'handlers': ['debug', 'console'],
                'level': 'DEBUG',
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    })


def django_monkey_patch(settings):
    _patch_models_to_dict()
    _patch_pymysql_as_mysqldb()
    if settings.DEBUG:
        _patch_windows_console_color()
    _patch_request_query_dict()
    _patch_logger(settings)
