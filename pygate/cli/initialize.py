import click
from .main import pygate


@pygate.group()
@click.pass_context
def init(ctx):
    pass


@init.command()
@click.pass_context
def mac(ctx):
    if ctx.obj['config'] is None:
        print('NONE')
    else:
        print(ctx.obj['config'])


# @click.command()
# @click.option('--config', '-c', type=str, default=c['pygate_config'], help='config YAML file name')
# @click.option('--pre', '-p', 'content', flag_value='pre', help='Initialize to pre make sub dirs.')
# @click.option('--dir', '-d', 'content', flag_value='sub', help='Make sub dirs')
# @click.option('--all', '-a', 'content', flag_value='all',  default=True, help='All tasks above')
# def init(config, content):
#     """
#     Initialize working directory
#     """
#     c = _load_config(config)
#     make_all = False
#     service.init(c, content)
