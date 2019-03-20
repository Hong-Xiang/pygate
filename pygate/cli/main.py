import click


def auto_sub():
    from ..conf import config, KEYS
    if config.get(KEYS.SUB_PATTERNS) is None:
        config[KEYS.SUB_PATTERNS] = [config.get(KEYS.SUB_PREFIX) + '*']
        config[KEYS.SUB_FORMAT] = config.get(KEYS.SUB_PREFIX) + r'.{}'


def load_config(filename, is_no_config, dryrun):
    from ..conf import config, KEYS
    import yaml
    import json
    if dryrun is not None:
        config['dryrun'] = dryrun
    if not is_no_config and filename is not None:
        with open(filename, 'r') as fin:
            if filename.endswith('yml'):
                config.update(yaml.load(fin))
            else:
                config.update(json.load(fin))
    auto_sub()


@click.group()
@click.option('--config', '-c', help="config file name", default=None)
@click.option('--no-config', help="ignore config file", is_flag=True)
@click.option('--dryrun', help='Do not do anything, just show expected results.', is_flag=True)
def pygate(config, no_config, dryrun):
    from dxl.fs import File
    if config is None:
        f = File('./pygate.yml')
        if f.exists():
            config = f.path.n
    if config is None:
        f = File('./pygate.json')
        if f.exists():
            config = f.path.n
    load_config(config, no_config, dryrun)


from .initialize import init


cli = pygate(obj={})

