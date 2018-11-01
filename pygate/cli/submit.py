import click
from ..conf import config, KEYS, SUBMIT_KEYS
from .main import pygate
from typing import Iterable, Tuple
# from dxl.cluster import Task, submit_task
# from dxl.cluster import TaskSlurm as TS
import os


# class TaskSlurm(TS):
#     def __init__(self, broadcast=None, single=None, user_task_id=None):
#         super().__init__()
#         self.broadcast = broadcast
#         self.single = single
#         self.user_task_id = user_task_id


def submit_kernel(tasks: Iterable, subdir_patterns: Iterable[str], dryrun):
    from pygate.routine import submit
    d = submit.Directory('')
    ops = []
    for t in tasks:
        if t[0] is not None:
            ops.append(submit.OpSubmitBroadcast(t[0], subdir_patterns))
        if t[1] is not None:
            ops.append(submit.OpSubmitSingleFile(t[1]))
    r = submit.RoutineOnDirectory(d, ops, dryrun)
    r.work()
    print(r.last_result())
    return r.echo()


@pygate.command()
@click.option('--broadcast', '-b', multiple=True)
@click.option('--single', '-s', multiple=True)
def submit(broadcast, single):
    if len(broadcast) == 0 and len(single) == 0:
        submit_conf = config.get(KEYS.SUBMIT, {})
        broadcast = submit_conf.get(SUBMIT_KEYS.BROADCAST)
        single = submit_conf.get(SUBMIT_KEYS.SINGLE)
        tasks = [(b, s) for b, s in zip(broadcast, single)]
        click.echo(submit_kernel(tasks, config.get(KEYS.SUB_PATTERNS),
                                 config.get(KEYS.DRYRUN)))

    return

    # if len(broadcast) == 0 and len(single) == 0:
    #     submit_conf = config.get(KEYS.SUBMIT, {})
    #     # from pygate.routine import submit
    #     # d = submit.Directory('.')
    #     # task_father = Task(workdir=d.path.s) # removes: is_root=True, desc='father'
    #     user_task = Task(details={"workdir": os.getcwd(),
    #                               "is_user_task": True,
    #                               "script": "post.sh"})
    #
    #     user_task_id = submit_task(user_task).id
    #     broadcast = submit_conf.get(SUBMIT_KEYS.BROADCAST)
    #     single = submit_conf.get(SUBMIT_KEYS.SINGLE)
    #
    #     print(f"************use_task_id, broadcast, single")
    #     print(f"User task id just submitted is : {user_task_id}")
    #     print(broadcast)
    #     print(single)
    #
    #     tasks = [Task(b, s, user_task_id) for b, s in zip(broadcast, single)]
    #     print(f"Number of tasks is : {len(tasks)}")
    #
    #     from dxl.cluster.database2.model import taskSlurmSchema
    #     # print(f"************task: {taskSlurmSchema.dump(tasks[0])}")
    #     print(f"************task: {tasks[0].to_json()}")
    #     click.echo(submit_kernel(tasks, config.get(KEYS.SUB_PATTERNS),
    #                              config.get(KEYS.DRYRUN)))