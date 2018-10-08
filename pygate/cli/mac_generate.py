import click
from .initialize import generate
from ..utils.syscall import shell_call


@generate.group()
def mac():
    """
    Generate mac file.
    """


@mac.command()
@click.option('--target', '-t', help="Filename of script to run to generate mac file.")
@click.option('--config', '-c', help="config filename to generate macs.")
@click.option('--output', '-o', help="MAC filename, will passed to script or predefined method.", default='main.mac')
def script(target, output, config):
    """
    Generate mac file by running a .py file.
    """
    if config is not None:
        shell_call('python {} --output {} --config {}'.format(target, output, config))
    else:
        shell_call(f'python {target} --output {output}')


@mac.command()
@click.option('--predefined', '-p', help="Name of predefined system to generate mac file.")
@click.option('--config', '-c', help="config filename to generate macs.")
@click.option('--target', '-t', help="MAC filename, will passed to script or predefined method.")
def predefined(target, config):
    """
    Generate mac file by predefined system.
    """
    raise NotImplementedError
