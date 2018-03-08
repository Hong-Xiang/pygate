import click


def auto_sub():
    from ..conf import config, KEYS
    if config.get(KEYS.SUB_PATTERNS) is None:
        config[KEYS.SUB_PATTERNS] = [config.get(KEYS.SUB_PREFIX) + '*']
        config[KEYS.SUB_FORMAT] = config.get(KEYS.SUB_PREFIX) + r'.{}'


def load_config(filename, is_no_config, dryrun):
    from ..conf import config, KEYS
    if dryrun is not None:
        config['dryrun'] = dryrun
    if not is_no_config:
        pass
    auto_sub()


@click.group()
@click.option('--config', '-c', help="config file name", default='pygate.yml')
@click.option('--no-config', help="ignore config file", is_flag=True)
@click.option('--dryrun', help='Do not do anything, just show expected results.', is_flag=True)
def pygate(config, no_config, dryrun):
    load_config(config, no_config, dryrun)


from .clean import clean
from .initialize import init
from .analysis import analysis
from .merge import merge
from .submit import submit
# class CLI(click.MultiCommand):
#     commands = {'init': None,
#                 'merge': None,
#                 'clean': None,
#                 'analysis': None,
#                 'submit': None}

#     def __init__(self):
#         super(__class__, self).__init__(name='pygate', help=__class__.__doc__)

#     def list_commands(self, ctx):
#         return sorted(self.commands.keys())

#     def get_command(self, ctx, name):
#         from .initialize import init
#         from .analysis import analysis
#         from .merge import merge
#         from .clean import clean
#         from .submit import submit
#         cmd_map = {
#             'init': init,
#             'merge': merge,
#             'clean': clean,
#             'submit': submit,
#             'analysis': analysis
#         }
#         if name in self.commands and self.commands[name] is None:
#             self.commands[name] = cmd_map[name]
#         return self.commands.get(name)

cli = pygate(obj={})

# pygate = CLI()
