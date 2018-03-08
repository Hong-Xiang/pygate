import click
from ..conf import config, KEYS, SUBMIT_KEYS
from .main import pygate


@pygate.command()
@click.option('--broadcast', '-b', multiple=True)
@click.option('--single', '-s', multiple=True)
def submit(broadcast, single):
    from pygate.routine import submit
    if len(broadcast) == 0 and len(single) == 0:
        submit_conf = config.get(KEYS.SUBMIT, {})
        broadcast = submit_conf.get(SUBMIT_KEYS.BROADCAST)
        single = submit_conf.get(SUBMIT_KEYS.SINGLE)
        d = submit.Directory('.')
        ops = []
        for b, s in zip(broadcast, single):
            ops.append(submit.OpSubmitBroadcast(b,
                                                config.get(KEYS.SUB_PATTERNS)))
            ops.append(submit.OpSubmitSingleFile(s))
        r = submit.RoutineOnDirectory(d, ops, config.get(KEYS.DRYRUN))
        r.work()
        click.echo(r.echo())
