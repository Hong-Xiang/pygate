from typing import Iterable


def shell_call(commands: Iterable[str] or str, is_echo=True):
    """
    Parameters:

    - `command`: Command to be executed.
    - `is_echo`: If True, print stdout and stderr of command to current stdout and stderr.
    """
    import subprocess
    import sys

    if isinstance(commands, str):
        commands = [commands]
    with subprocess.Popen(commands,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True) as p:
        out = p.stdout.read().decode()
        err = p.stderr.read().decode()
        if is_echo:
            sys.stdout.write(out)
            sys.stderr.write(err)
    return {'out': out, 'err': err}
