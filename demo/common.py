# coding=utf-8
import logging
from demo.conf import CONF

log = logging.getLogger(__name__)


class Demo(object):

    def __init__(self, init=None):
        self.init = init or dict(CONF.site)

    def run(self, *args, **kw):
        log.debug('init=%s, args=%s, kw=%s', self.init, args, kw)
