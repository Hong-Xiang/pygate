import click
from .main import pygate


@pygate.command()
@click.option('--target', '-t', multiple=True)
@click.option('--method', '-m', multiple=True)
def merge(target, method):
    

    pass
