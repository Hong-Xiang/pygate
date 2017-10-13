#!/home/hongxwing/anaconda3/bin/python
import click
import yaml
from fs.osfs import OSFS
import os
import subprocess
import sys
from pygate import service

DEFAULT_CONFIG_FILE = service.ConfigMaker.DEFAULT_CONFIG_FILENAME


@click.group()
def gate():
    pass


@gate.command()
@click.option('--target', '-t', type=str, default='.', help='target directory')
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config file name')
def make_config(target, config):
    service.ConfigMaker.make(target, config)


def load_config(config):
    with open(config) as fin:
        return yaml.load(fin)


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
@click.option('--templates', '-t', 'content', flag_value='templates', help='copy files from template directory')
@click.option('--shell', '-s', 'content', flag_value='shell', help='generate shell files')
@click.option('--dirs', '-d', 'content', flag_value='dirs', help='generate and copy files to sub directories')
@click.option('--macss', '-m', 'content', flag_value='macs', help='generate mac files')
@click.option('--all', '-a', 'content', flag_value='all',
              default=True, help='All tasks above')
def init(config, content):
    """
    Initialize working directory
    """
    c = load_config(config)
    make_all = False
    if content == 'all':
        make_all = True
    if content == 'macs' or make_all:
        service.Initializer.mac(c)
    if content == 'templates' or make_all:
        service.Initializer.templates(c)
    if content == 'shell' or make_all:
        service.ShellMaker.run(c)
        service.ShellMaker.post(c)
        # service.make_run_sh(c['target'], c['run_sh'],
        #                     c['main_mac'], c['analysis_c'])
        # service.make_post_sh(c['target'], c['post_sh'])
    if content == 'dirs' or make_all:
        service.SubDirectoryMaker.make_subs(c)


@click.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config file name')
def run(config):
    c = load_config(config)
    service.run(c['target'], c['main_mac'], stdout=c['stdout'])


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
def submit(config):
    # TODO: add submit service
    c = load_config(config)
    service.Submitter.submit(c)


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
def merge(config):
    c = load_config(config)
    service.Merger.merge(c)


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
@click.option('--dirs', '-d', 'content', flag_value='dirs', default=True)
@click.option('--all', '-a', 'content', flag_value='all')
@click.option('--dryrun', is_flag=True)
def clear(config, content, dryrun):
    c = load_config(config)
    if content == 'dirs':
        service.Cleaner.subs(c, dryrun)
    elif content == 'all':
        service.Cleaner.all(c, dryrun)


if __name__ == "__main__":
    gate()
