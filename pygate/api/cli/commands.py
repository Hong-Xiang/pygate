import click
from ...config import config as c
from ... import service


def _load_config(config):
    import yaml
    with open(config) as fin:
        return yaml.load(fin)


@click.command()
def make_config():
    service.make_config()


@click.command()
@click.option('--config', '-c', type=str, default=c['pygate_config'], help='config YAML file name')
@click.option('--pre', '-p', 'content', flag_value='pre', help='Initialize to pre make sub dirs.')
@click.option('--dir', '-d', 'content', flag_value='sub', help='Make sub dirs')
@click.option('--all', '-a', 'content', flag_value='all',  default=True, help='All tasks above')
def init(config, content):
    """
    Initialize working directory
    """
    c = _load_config(config)
    make_all = False
    service.init(c, content)



