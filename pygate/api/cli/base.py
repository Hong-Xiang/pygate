import click


class CLI(click.MultiCommand):
    """
    PYGATE: A simplified python interface of gate.
    """
    commands = {'make_config': None,
                'init': None,
                'submit': None,
                'merge': None,
                'clean': None}

    def __init__(self):
        super(__class__, self).__init__(name='pygate', help=__class__.__doc__)

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from . import commands
        if name in self.commands and self.commands[name] is None:
            self.commands[name] = getattr(commands, name)
        return self.commands.get(name)


main = CLI()
