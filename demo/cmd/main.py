# coding=utf-8
import sys
import demo.conf
from demo.common import Demo

CONF = demo.conf.CONF


def main():
    demo.conf.init(sys.argv)
    obj = Demo(dict(CONF.site))
    obj.run('demo', 'args', de='mo')


if __name__ == '__main__':
    sys.exit(main())
