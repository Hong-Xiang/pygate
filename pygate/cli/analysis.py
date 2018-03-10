import click
from .main import pygate
from ..conf import config, KEYS


def analysis_kernel(source, target, analysis_type, dryrun):
    from pygate.routine.analysis import OperationAnalysis
    from pygate.routine.base import RoutineOnDirectory
    from dxl.fs import Directory
    d = Directory('.')
    o = OperationAnalysis(source, target, analysis_type)
    r = RoutineOnDirectory(d, [o])


@pygate.command()
@click.option('--analysis-type', '-a', help="Predifined analysis workflow.")
@click.option('--source', '-s', help="Analysis source data filename.")
@click.option('--target', '-t', help="Analysis target data filename.")
def analysis(analysis_type, source, target):
    analysis_type = analysis_type or conf.KEYS.AN
    analysis_kernel()
