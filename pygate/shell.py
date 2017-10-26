import sys
import warnings
from fs.osfs import OSFS
from collections import OrderedDict


class Defaults:
    SHELL = 'zsh'


class Snippets:
    SHELL = {
        'bash': r'#!/bin/bash',
        'zsh': r"#!/usr/bin/zsh"
    }

    SOURCE = {
        'bash': r'~/.bashrc',
        'zsh': r'~/.zshrc'
    }

    SBATCH = ["#SBATCH -o %J.out",
              "#SBATCH -e %J.err"]

    @classmethod
    def add_task_func(cls, key):
        TASK_MAPPING = {
            'GATE': cls.add_gate,
            'ROOT': cls.add_root,
            'HADD': cls.add_hadd,
            'CLEARSUB': cls.add_clear_sub,
            'MERGE': cls.add_merge}
        return TASK_MAPPING.get(key.upper())

    @classmethod
    def add_shell(cls, scripts, name):
        name = name.lower()
        if not name in cls.SHELL:
            fmt = 'Unknown shell name {0}, use {1} instead.'
            warnings.warn(fmt.format(name, Defaults.SHELL), RuntimeWarning)
            name = Defaults.SHELL
        scripts.append(cls.SHELL[name])

    @classmethod
    def add_source(cls, scripts, name):
        name = name.lower()
        if not name in cls.SHELL:
            fmt = 'Unknown shell name {0}, use {1} instead.'
            warnings.warn(fmt.format(name, Defaults.SHELL), RuntimeWarning)
            name = Defaults.SHELL
        scripts.append('source ' + cls.SOURCE[name])

    @classmethod
    def add_sbatch(cls, scripts):
        for s in cls.SBATCH:
            scripts.append(s)

    @classmethod
    def add_gate(cls, scripts, filename):
        scripts.append('Gate {0}'.format(filename))

    @classmethod
    def add_root(cls, scripts, filename):
        scripts.append('root -q -b {0}'.format(filename))

    @classmethod
    def add_hadd(cls, scripts, target, filenames):
        if isinstance(filenames, str):
            filenames = [filenames]
        scripts.append('hadd {0} '.format(target) + ' '.join(filenames))

    @classmethod
    def add_merge(cls, scripts):
        scripts.append('pygate merge')

    @classmethod
    def add_clear_sub(cls, scripts):
        scripts.append('pygate clear --dirs')

    @classmethod
    def add_task(cls, scripts, task_name, payloads):
        add_func = cls.add_task_func(task_name)
        if add_func is None:
            fmt = 'Unknown task name {0}, skipped.'
            warnings.warn(fmt.format(task_name), RuntimeWarning)
            return
        payloads = payloads or {}
        add_func(scripts, **payloads)


def _load_shell_template(task_type, shell):
    from .utils import load_script
    import jinja2
    task_type = task_type.lower()
    if not task_type in ['map', 'merge']:
        raise ValueError("Task type {} is not supported.".format(task_type))
    shell = shell.lower()
    if not shell in ['bash', 'zsh']:
        raise ValueError("Shell {} is not supported.".format(task_type))
    script_name = "{0}_{1}.sh".format(task_type, shell)
    return jinja2.Template(load_script(script_name))


def _get_workdir_on_local_and_server(path_workdir):
    from dxpy.filesystem import Path
    p_ser = Path(path_workdir).abs
    p_loc = (Path('~/Slurm/') / Path(path_workdir).rel).rel
    return p_ser, p_loc


def _add_gate(commands, task):
    if task.get('method') == 'Gate':
        commands.append("Gate {}".format(task['filename']))


def _add_root(commands, task):
    if task['method'] == 'root':
        commands.append("root -q -b {}".format(task['filename']))


MAP_TASKS = [_add_gate, _add_root]


def _make_commands(task_type, tasks):
    commands = ['']
    if task_type == 'map':
        for t in tasks:
            for add_cmd in MAP_TASKS:
                add_cmd(commands, t)
    commands.append('')
    return "\n".join(commands)


def make(fs, workdir: str, task_type: str, tasks=None, shell='zsh'):
    scrpt_tpl = _load_shell_template(task_type, shell)
    p_ser, p_loc = _get_workdir_on_local_and_server(fs.getsyspath(workdir))
    return scrpt_tpl.render(local_work_directory=p_loc,
                            server_work_directory=p_ser,
                            commands=_make_commands(task_type, tasks))


class ShellScript:
    def __init__(self, workdir=None, task_type='map', tasks=None, shell='zsh'):
        self.workdir = workdir
        if not task_type.lower() in ['map', 'merge']:
            raise ValueError(
                "Task type {} is not supported.".format(task_type))
        self.task_type = task_type.lower()
        if not shell.lower() in ['bash', 'zsh']:
            raise ValueError("Shell {} is not supported.".format(task_type))
        self.shell = shell.lower()
        self.tasks = tasks or []
        self._make()

    def dump(self):
        if isinstance(self.output, str):
            with OSFS('.') as fs:
                with fs.open(self.output, 'w') as fout:
                    print('\n'.join(self.scripts), file=fout)
        else:
            print('\n'.join(self.scripts), file=self.output)

    def add_head(self):
        Snippets.add_shell(self.scripts, self.shell)
        Snippets.add_sbatch(self.scripts)
        Snippets.add_source(self.scripts, self.shell)
        self.scripts.append('hostname')
        self.scripts.append('date')

    def add_tasks(self):
        for t in self.tasks:
            Snippets.add_task(self.scripts, t.get('name'), t.get('payloads'))

    def add_tail(self):
        self.scripts.append('date')
        self.scripts.append('')
