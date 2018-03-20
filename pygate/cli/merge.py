import click
from .main import pygate
from typing import Iterable

from ..conf import config, KEYS, SUBMIT_KEYS


class Task:
    def __init__(self, filename, method):
        self.filename = filename
        self.method = method


def merge_kernel(tasks: Iterable[Task], subdir_pattern: Iterable[str], dryrun):
    from pygate.routine import merger as merge
    d = merge.Directory('.')
    op_map = {
        'hadd': merge.OpMergeHADD,
        'cat': merge.OpMergeCat,
        'sum_bin': merge.OpMergeSumBinary,
        'catpdh5': merge.OpMergePandasConcatenate
    }
    ops = [op_map[t.method.lower()](t.filename, subdir_pattern) for t in tasks]
    r = merge.RoutineOnDirectory(d, ops, dryrun)
    r.work()
    return r.echo()


@pygate.command()
@click.option('--target', '-t', multiple=True)
@click.option('--method', '-m', multiple=True)
def merge(target, method):
    tasks = [Task(t, m) for t, m in zip(target, method)]
    click.echo(merge_kernel(tasks, config.get(KEYS.SUB_PATTERNS),
                            config.get(KEYS.DRYRUN)))
