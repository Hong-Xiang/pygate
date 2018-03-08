import click

from .main import pygate


@pygate.command()
@click.option('--subdirectories', '-d', )
def clean():
    pass
