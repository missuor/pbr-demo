# coding=utf-8
import os
import sys
import imp
from django.conf import global_settings as gs
from django.conf.urls import url
from django.conf.urls import include
from django.core.wsgi import get_wsgi_application
from django.views import static
from demo.utils import django_monkey_patch
from demo.conf import CONF

DEBUG = CONF.debug
LOCATION_PREFIX = 'demo'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = CONF.site.static_root
MEDIA_ROOT = CONF.site.media_root
LOG_PATH = CONF.site.log_path
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

app_settings = {
    'INSTALLED_APPS': [
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'demo',
    ],
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                '',
                os.path.join(BASE_DIR, 'templates'),
                'django.template.loaders.filesystem.Loader'
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    # 'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    'DEBUG': DEBUG,
    'SECRET_KEY': '-&y97w=x$0&u-zap#amh&&-$$ygiw)h%9mp^%8*t+)(cf#1iu&',
    'ALLOWED_HOSTS': ['*'],
    'WSGI_APPLICATION': 'demo.wsgi.application',
    'STATICFILES_DIRS': DEBUG and ['', STATIC_ROOT] or None,
    'STATIC_ROOT': not DEBUG and STATIC_ROOT or None,
    'LOG_PATH': LOG_PATH,
    'MEDIA_ROOT': MEDIA_ROOT,
    'ROOT_URLCONF': 'demo.urls',
    'STATIC_URL': '/demo/static/',
    'LANGUAGE_CODE': 'zh-hans',
    'TIME_ZONE': 'Asia/Shanghai',
    'LOCATION_PREFIX': LOCATION_PREFIX,
}

custom_settings = {k: v for k, v in vars(gs).items() if not k.startswith('_') and not callable(v)}
custom_settings.update(app_settings)
settings = imp.new_module('settings')
for k, v in custom_settings.items():
    setattr(settings, k, v)

urls = imp.new_module('urls')
urls.urlpatterns = [
    url(r'^demo/', include('demo.views', namespace='demo')),
    url(r'^demo/static/(?P<path>.*)$', static.serve, {
        'document_root': STATIC_ROOT,
        'show_indexes': True
    }),
]

sys.modules['demo.settings'] = settings
sys.modules['demo.urls'] = urls
django_monkey_patch(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
application = get_wsgi_application()

__all__ = ['application']
