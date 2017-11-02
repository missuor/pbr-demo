# coding=utf-8
from oslo_config import cfg
from demo import version


default_opts = [
    cfg.StrOpt('debug', default=False, help='Whether to open debug model.'),
]


site_opts = [
    cfg.StrOpt('static_root', default='/var/www/demo/static', help='The site static_root.'),
    cfg.StrOpt('media_root', default='/var/www/demo/static/media', help='The site media_root.'),
    cfg.StrOpt('log_path', default='/var/logs/demo', help='The site log_path.'),
]


site_group = cfg.OptGroup(name='site', title='Options for the Site')

CONF = cfg.CONF
CONF.register_group(site_group)

CONF.register_opts(default_opts)
CONF.register_opts((site_opts), site_group)


def init(argv=None, default_config_files=None):
    argv = argv or []
    CONF(argv[1:], project='demo', version=version.version_info.release_string(), default_config_files=default_config_files)

init()

__all__ = ['CONF', 'init']
