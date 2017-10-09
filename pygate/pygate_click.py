#!/home/hongxwing/anaconda3/bin/python
import click
import yaml
from fs.osfs import OSFS
import os
import subprocess
import sys
from pygate import service


@click.group()
def gate():
    pass


DEFAULT_CONFIGS = {
    'template_source_directory': os.environ.get('PATH_MACS_TEMPLATES',
                                                '/hqlf/hongxwing/macs_template'),
    'target': '.',
    'group_name': 'Ecat',
    'main_mac': 'PET_Ecat.mac',
    'analysis_c': 'PET_Analyse.C',
    'nb_split': 10,
    'merge_file': 'polyEcat.txt',
    'no_action': False,
    'run_sh': 'run.sh',
    'post_sh': 'post.sh'
}

DEFAULT_CONFIG_FILE = 'config.yml'


@gate.command()
@click.option('--target', '-t', type=str, default='.', help='target directory')
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config file name')
def generate_config(target, config):
    with OSFS(target) as t:
        with t.open(config, 'w') as fout:
            yaml.dump(DEFAULT_CONFIGS, fout, default_flow_style=False)


def load_config(config):
    with open(config) as fin:
        return yaml.load(fin)


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
@click.option('--templates', '-t', 'content', flag_value='templates')
@click.option('--shell', '-s', 'content', flag_value='shell')
@click.option('--dirs', '-d', 'content', flag_value='dirs')
@click.option('--all', '-a', 'content', flag_value='all',
              default=True)
def init(config, content):
    c = load_config(config)
    make_all = False
    if content == 'all':
        make_all = True
    if content == 'templates' or make_all:
        service.copy_group(c['template_source_directory'],
                           c['target'],
                           c['group_name'])
    if content == 'shell' or make_all:
        service.make_run_sh(c['target'], c['run_sh'],
                            c['main_mac'], c['analysis_c'])
        service.make_post_sh(c['target'], c['post_sh'])
    if content == 'dirs' or make_all:
        service.make_subs(c['target'], c['nb_split'])


@click.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config file name')
def run(config):
    c = load_config(config)
    service.run(c['target'], c['main_mac'], stdout=c['stdout'])


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
@click.option('--print', '-p', 'worker', flag_value='print', default=True)
@click.option('--slurm', '-s', 'worker', flag_value='slurm')
@click.option('--hqlf', '-h', 'worker', flag_value='hqlf')
def submit(config, worker):
    # TODO: add submit service
    c = load_config(config)
    if worker == 'print':
        service.submit(c['target'], c['run_sh'], c['post_sh'],
                       service.submit_service_print)
    elif worker == 'direct':
        service.submit(c['target'], c['run_sh'], c['post_sh'],
                       service.submit_service_direct)
    elif worker == 'hqlf':
        service.submit(c['target'], c['run_sh'], c['post_sh'],
                       service.submit_service_hqlf)


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
def merge(config):
    c = load_config(config)
    service.merge(c['target'], c['merge_file'])


@gate.command()
@click.option('--config', '-c', type=str, default=DEFAULT_CONFIG_FILE, help='config YAML file name')
@click.option('--dirs', '-d', 'content', flag_value='dirs', default=True)
@click.option('--all', '-a', 'content', flag_value='all')
@click.option('--dryrun', is_flag=True)
def clear(config, content, dryrun):
    c = load_config(config)
    if content == 'dirs':
        service.clear_subdirs(c['target'], dryrun)
    elif content == 'all':
        service.clear_all(c['target'], config, dryrun)


if __name__ == "__main__":
    gate()
