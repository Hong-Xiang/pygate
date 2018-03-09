"""
Initialization CLI support.

Note many configurations is done by config file. 
"""
import click
from .main import pygate
from ..conf import config, KEYS, INIT_KEYS
import json
import yaml
from dxl.fs import File, Directory


@pygate.group()
def init():
    pass


@pygate.group()
def generate():
    pass


@generate.command()
@click.option('--script', '-s', help="Filename of script to run to generate mac file.")
@click.option('--mac-config', '-c', help="Config filename to generate predefined macs.")
@click.option('--target', '-t', help="MAC filename.")
@click.option('--no-broadcast', '-n', help="Do not add broadcast flag of mac to pygate config.", is_flag=True)
def mac(script, mac_config, target, no_broadcast):
    """
    Generate mac file.
    """
    pass


def shell_run(filename, tasks, gate_version, shell):
    from pygate.scripts.shell import ScriptRun, GateSimulation, RootAnalysis
    SKS = INIT_KEYS.SHELL_KEYS
    task_list = []
    for t in tasks:
        name = t[SKS.TASK_NAME]
        if name == SKS.GATE_SIMULATION:
            task_list.append(GateSimulation(t[SKS.TARGET]))
        else:
            raise ValueError("Unknown task name {}.".format(name))

    shell_script = ScriptRun(Directory('.').system_path(), task_list,
                             gate_version, shell)
    with open(filename, 'w') as fout:
        print(shell_script.render(), file=fout)


def shell_post_run(filename, tasks, shell):
    from pygate.scripts.shell import ScriptPostRun, Merge, RootAnalysis
    SKS = INIT_KEYS.SHELL_KEYS
    task_list = []
    for t in tasks:
        name = t[SKS.TASK_NAME]
        if name == SKS.MERGE:
            task_list.append(Merge(t[SKS.TARGET], t[SKS.METHOD]))
        elif name == SKS.ROOT_ANALYSIS:
            task_list.append(RootAnalysis(t[SKS.TARGET]))
        else:
            raise ValueError("Unknown task name {}.".format(name))
    shell_script = ScriptPostRun(task_list, shell)
    with open(filename, 'w') as fout:
        print(shell_script.render(), file=fout)


@generate.command()
def shell():
    """
    Generate shell script, pre run or post run.
    """
    SKS = INIT_KEYS.SHELL_KEYS
    shellc = config.get(KEYS.INIT, {}).get(INIT_KEYS.SHELL)
    src = shellc.get(SKS.RUN)
    shell_run(src[SKS.TARGET], src[SKS.TASK],
              src[SKS.GATE_VERSION], src[SKS.SHELL_TYPE])
    sprc = shellc.get(SKS.POST_RUN)
    shell_post_run(sprc[SKS.TARGET], sprc[SKS.TASK],
                   sprc[SKS.SHELL_TYPE])


@generate.command()
@click.option('--target', '-t', help='Config file name.')
@click.option('--format', '-f', help='Format of config file, json or yml')
def cfg(target, format):
    """
    Generate initial config file.
    """
    from dxl.fs import Path
    if target is None and format is None:
        target = 'pygate.yml'
    if format is None:
        format = Path(target).e
    if target is None:
        target = 'pygate.{}'.format(format)
    if format.startswith('.'):
        format = format[1:]
    with open(target, 'w') as fout:
        if format.lower() == 'yml':
            yaml.dump(config, fout)
        elif format.lower() == 'json':
            json.dump(config, fout, indent=4, sort_keys=True)


@init.command()
@click.option('--nb-split', '-n', type=int, help='Number of subdirectories.')
@click.option('--sub-format', '-f', help='Subdirectories format str.')
def subdir(nb_split, sub_format):
    from pygate.routine.initialize import OpSubdirectoriesMaker, RoutineOnDirectory
    if nb_split is None:
        nb_split = config.get(KEYS.NB_SPLIT)
    if sub_format is None:
        sub_format = config.get(KEYS.SUB_FORMAT)
    d = Directory('.')
    op = OpSubdirectoriesMaker(nb_split, sub_format)
    r = RoutineOnDirectory(d, [op], config.get(KEYS.DRYRUN))
    r.work()
    click.echo(r.echo())


def broadcast_kernel(files, subdirectory_patterns, dryrun):
    from pygate.routine.initialize import OpAddToBroadcastFile, OpBroadcastFile, RoutineOnDirectory
    d = Directory('.')
    ops = [OpAddToBroadcastFile(f) for f in files]
    ops.append(OpBroadcastFile(subdirectory_patterns))
    r = RoutineOnDirectory(d, ops, dryrun)
    r.work()
    return r.echo()


@init.command()
@click.option('--target', '-t', type=int, help='Files to broadcast to subdirectories.', multiple=True)
@click.option('--add-ext', '-e', help='Include all external files.', is_flag=True)
def bcast(target, add_ext):
    from ..conf import BROADCAST_KEYS
    files = config.get(KEYS.BROADCAST, {}).get(BROADCAST_KEYS.TARGETS, ())
    if config.get(KEYS.BROADCAST, {}).get(BROADCAST_KEYS.ADD_EXT):
        files = list(files) + [e[1] for e in external_to_copy()]
    click.echo(broadcast_kernel(files, config.get(KEYS.SUB_PATTERNS),
                                config.get(KEYS.DRYRUN)))


def external_to_copy():
    from dxl.fs import Path
    inic = config.get(KEYS.INIT)
    tasks = inic.get(INIT_KEYS.EXTERNAL)
    if tasks is None:
        return ()
    result = []
    for t in tasks:
        source = t[INIT_KEYS.EXTERNAL_KEYS.SOURCE]
        target = t.get(INIT_KEYS.EXTERNAL_KEYS.TARGET,
                       './' + Path(source).n)
        result.append((source, target))
    return result


@init.command()
def ext():
    """
    Copy external files.
    """
    inic = config.get(KEYS.INIT)
    tasks = inic.get(INIT_KEYS.EXTERNAL)
    import shutil
    import json
    results = []
    for t in external_to_copy():
        source = t[0]
        target = t[1]
        shutil.copyfile(source, target)
        results.append({INIT_KEYS.EXTERNAL_KEYS.SOURCE: source,
                        INIT_KEYS.EXTERNAL_KEYS.TARGET: target})
    results = json.dumps(results, indent=4, separators=(',', ': '))
    click.echo(results)


@init.command()
def auto():
    pass


# @click.command()
# @click.option('--config', '-c', type=str, default=c['pygate_config'], help='config YAML file name')
# @click.option('--pre', '-p', 'content', flag_value='pre', help='Initialize to pre make sub dirs.')
# @click.option('--dir', '-d', 'content', flag_value='sub', help='Make sub dirs')
# @click.option('--all', '-a', 'content', flag_value='all',  default=True, help='All tasks above')
# def init(config, content):
#     """
#     Initialize working directory
#     """
#     c = _load_config(config)
#     make_all = False
#     service.init(c, content)
