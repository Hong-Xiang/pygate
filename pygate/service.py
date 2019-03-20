"""
Warp of supported methods, set their working filesystem to current directory.
"""
from fs.osfs import OSFS


def make_config(target='.'):
    from .config_maker import ConfigMaker
    from .config import config as c
    with OSFS('.') as fs:
        ConfigMaker.make(fs, '.')


def init(config, method):
    from .initializer import Initializer
    with OSFS('.') as fs:
        initer = Initializer(fs, config)
        if method == 'pre' or method == 'all':
            initer.pre_sub()
        if method == 'sub' or method == 'all':
            initer.make_sub()


