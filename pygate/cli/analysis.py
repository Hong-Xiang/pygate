import click
from .main import pygate
from ..conf import config, KEYS 

@pygate.command()
@click.option('--analysis-type', '-a', help="Predifined analysis workflow.")
@click.option('--source', '-s', help="Analysis source data filename.")
@click.option('--target', '-t', help="Analysis target data filename.")
def analysis(analysis_type, source, target):
    pass
