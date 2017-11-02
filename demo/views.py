# coding=utf-8
import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf.urls import url
from demo.common import Demo

logger = logging.getLogger(__name__)


def demo(request, action=None):
    logger.debug('action=%s', action)
    if not action:
        return redirect(reverse('demo:action', args=['hello-world']))

    else:
        obj = Demo(action)
        obj.run()
        return render(request, 'action.html', {'action': action})


urlpatterns = [
    url(r'^$', demo, name='index'),
    url(r'^(?P<action>[\w-]+)/?$', demo, name='action'),
]
