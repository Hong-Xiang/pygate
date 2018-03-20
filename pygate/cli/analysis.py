import click
from .main import pygate
from ..conf import config, KEYS
from ..utils.syscall import shell_call


def analysis_kernel(source, target, analysis_type, dryrun):
    from pygate.routine.analysis import OperationAnalysis
    from pygate.routine.base import RoutineOnDirectory
    from dxl.fs import Directory
    d = Directory('.')
    o = OperationAnalysis(source, target, analysis_type)
    r = RoutineOnDirectory(d, [o])
    r.work()
    return r.echo()


@pygate.group()
def analysis():
    pass


@analysis.command()
@click.option('--name', '-n', help="Predefined analysis type name.")
@click.option('--source', '-s', help="Analysis source data filename.")
@click.option('--output', '-o', help="Analysis target data filename.")
def predefined(name, source, output):
    click.echo(analysis_kernel(source, output, name, config.get(KEYS.DRYRUN)))


@analysis.command()
@click.option('--target', '-t', help="Analysis .py filename.")
@click.option('--source', '-s', help="Analysis source data filename.")
@click.option('--output', '-o', help="Output filename.")
def script(target, source, output):
    shell_call('python {} --source {} --output {}'.format(target, source, output))
