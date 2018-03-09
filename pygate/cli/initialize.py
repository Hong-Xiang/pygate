"""
Initialization CLI support.

Note many configurations is done by config file. 
"""
import click
from .main import pygate
from ..conf import config, KEYS, INIT_KEYS


@pygate.group()
def init():
    pass


@init.command()
@click.option('--script', '-s', help="Filename of script to run to generate mac file.")
@click.option('--mac-config', '-c', help="Config filename to generate predefined macs.")
@click.option('--target', '-t', help="MAC filename.")
@click.option('--no-broadcast', '-n', help="Do not add broadcast flag of mac to pygate config.", is_flag=True)
def mac(script, mac_config, target, no_broadcast):
    """
    Generate mac file.
    """
    pass


@init.command()
def shell(script, mac_config, target, no_broadcast):
    """
    Generate shell script, pre run or post run.
    """
    pass


@init.command()
def ext():
    """
    Copy external files.
    """
    inic = config.get(KEYS.INIT)
    tasks = inic.get(INIT_KEYS.EXTERNAL)
    import shutil
    import json
    from dxl.fs import Path
    results = []
    if tasks is not None:
        for t in tasks:
            source = t[INIT_KEYS.EXTERNAL_KEYS.SOURCE]
            target = t.get(INIT_KEYS.EXTERNAL_KEYS.TARGET,
                           './' + Path(source).n)
            shutil.copyfile(source, target)
            results.append({INIT_KEYS.EXTERNAL_KEYS.SOURCE: source,
                            INIT_KEYS.EXTERNAL_KEYS.TARGET: target})
    results = json.dumps(results, indent=4, separators=(',', ': '))
    click.echo(results)


@init.command()
def auto():
    pass


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
