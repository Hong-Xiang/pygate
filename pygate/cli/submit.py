import click
from ..conf import config, KEYS, SUBMIT_KEYS
from .main import pygate
from typing import Iterable, Tuple


class Task:
    def __init__(self, broadcast=None, single=None):
        self.broadcast = broadcast
        self.single = single


def submit_kernel(tasks: Iterable[Task], subdir_patterns: Iterable[str], dryrun):
    from pygate.routine import submit
    d = submit.Directory('.')
    ops = []
    for t in tasks:
        if t.broadcast is not None:
            ops.append(submit.OpSubmitBroadcast(t.broadcast,
                                                subdir_patterns))
        if t.single is not None:
            ops.append(submit.OpSubmitSingleFile(t.single))
    r = submit.RoutineOnDirectory(d, ops, dryrun)
    r.work()
    return r.echo()


@pygate.command()
@click.option('--broadcast', '-b', multiple=True)
@click.option('--single', '-s', multiple=True)
def submit(broadcast, single):
    if len(broadcast) == 0 and len(single) == 0:
        submit_conf = config.get(KEYS.SUBMIT, {})
        broadcast = submit_conf.get(SUBMIT_KEYS.BROADCAST)
        single = submit_conf.get(SUBMIT_KEYS.SINGLE)
        tasks = [Task(b, s) for b, s in zip(broadcast, single)]
        click.echo(submit_kernel(tasks, config.get(KEYS.SUB_PATTERNS),
                                 config.get(KEYS.DRYRUN)))
