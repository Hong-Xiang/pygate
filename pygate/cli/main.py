import click


class CLI(click.MultiCommand):
    commands = {'init': None,
                'merge': None,
                'clean': None,
                'analysis': None,
                'submit': None}

    def __init__(self):
        super(__class__, self).__init__(name='pygate', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from .initialize import init
        from .analysis import analysis
        from .merge import merge
        from .clean import clean
        from .submit import submit
        cmd_map = {
            'init': init,
            'merge': merge,
            'clean': clean,
            'submit': submit,
            'analysis': analysis
        }
        if name in self.commands and self.commands[name] is None:
            self.commands[name] = cmd_map[name]
        return self.commands.get(name)


pygate = CLI()
