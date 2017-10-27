# import sys
# import warnings
# from fs.osfs import OSFS
# from collections import OrderedDict


# class Defaults:
#     SHELL = 'zsh'


# class Snippets:
#     SHELL = {
#         'bash': r'#!/bin/bash',
#         'zsh': r"#!/usr/bin/zsh"
#     }

#     SOURCE = {
#         'bash': r'~/.bashrc',
#         'zsh': r'~/.zshrc'
#     }

#     SBATCH = ["#SBATCH -o %J.out",
#               "#SBATCH -e %J.err"]

#     @classmethod
#     def add_task_func(cls, key):
#         TASK_MAPPING = {
#             'GATE': cls.add_gate,
#             'ROOT': cls.add_root,
#             'HADD': cls.add_hadd,
#             'CLEARSUB': cls.add_clear_sub,
#             'MERGE': cls.add_merge}
#         return TASK_MAPPING.get(key.upper())

#     @classmethod
#     def add_shell(cls, scripts, name):
#         name = name.lower()
#         if not name in cls.SHELL:
#             fmt = 'Unknown shell name {0}, use {1} instead.'
#             warnings.warn(fmt.format(name, Defaults.SHELL), RuntimeWarning)
#             name = Defaults.SHELL
#         scripts.append(cls.SHELL[name])

#     @classmethod
#     def add_source(cls, scripts, name):
#         name = name.lower()
#         if not name in cls.SHELL:
#             fmt = 'Unknown shell name {0}, use {1} instead.'
#             warnings.warn(fmt.format(name, Defaults.SHELL), RuntimeWarning)
#             name = Defaults.SHELL
#         scripts.append('source ' + cls.SOURCE[name])

#     @classmethod
#     def add_sbatch(cls, scripts):
#         for s in cls.SBATCH:
#             scripts.append(s)

#     @classmethod
#     def add_gate(cls, scripts, filename):
#         scripts.append('Gate {0}'.format(filename))

#     @classmethod
#     def add_root(cls, scripts, filename):
#         scripts.append('root -q -b {0}'.format(filename))

#     @classmethod
#     def add_hadd(cls, scripts, target, filenames):
#         if isinstance(filenames, str):
#             filenames = [filenames]
#         scripts.append('hadd {0} '.format(target) + ' '.join(filenames))

#     @classmethod
#     def add_merge(cls, scripts):
#         scripts.append('pygate merge')

#     @classmethod
#     def add_clear_sub(cls, scripts):
#         scripts.append('pygate clear --dirs')

#     @classmethod
#     def add_task(cls, scripts, task_name, payloads):
#         add_func = cls.add_task_func(task_name)
#         if add_func is None:
#             fmt = 'Unknown task name {0}, skipped.'
#             warnings.warn(fmt.format(task_name), RuntimeWarning)
#             return
#         payloads = payloads or {}
#         add_func(scripts, **payloads)


# def _add_hadd(commands, fs, workdir, task):
#     from dxpy import batch
#     if task['method'] == 'hadd':
#         with fs.opendir(workdir) as d:
#             files = batch.files_in_directories(
#                 d, task['sub_dirs'], [task['filename']])
#             paths = [d.getsyspath(p) for p in files]
#             paths = [fs.getsyspath(p) for p in paths]
#         commands.append('hadd {0}'.format(
#             task['filename']) + ' '.join(paths))


# def _add_sum():
#     pass


# MAP_TASKS = [_add_gate, _add_root]


# def _make_commands(fs, workdir, task_type, tasks):
#     commands = ['']
#     if task_type == 'map':
#         for t in tasks:
#             for add_cmd in MAP_TASKS:
#                 add_cmd(commands, fs, workdir, t)
#     elif task_type == 'merge':
#         pass
#     commands.append('')
#     return "\n".join(commands)


# def _make_script_file(fs, workdir: str, output: str, task_type: str, tasks: list, shell='zsh'):
#     scrpt_tpl = __load_shell_template(task_type, shell)
#     p_ser, p_loc = _get_workdir_on_local_and_server(fs.getsyspath(workdir))
#     s = scrpt_tpl.render(local_work_directory=p_loc,
#                          server_work_directory=p_ser,
#                          commands=_make_commands(fs, workdir, task_type, tasks))
#     with fs.opendir(workdir) as d:
#         with d.open(output, 'w') as fout:
#             print(s, file=fout)


class ShellScriptBase:
    def __init__(self, fs, workdir: str, output: str, tasks: list, shell='zsh'):
        self.fs = fs
        self.workdir = workdir
        self.output = output
        self.tasks = tasks
        self.shell = shell.lower()
        if not self.shell in ['zsh', 'bash']:
            raise ValueError("Unknown shell {}.".format(self.shell))
        self.content = None
        self.task_type = None

    def _load_shell_template(self):
        from .utils import load_script
        import jinja2
        script_name = "{0}_{1}.sh".format(self.task_type, self.shell)
        return jinja2.Template(load_script(script_name))

    def _make(self):
        raise NotImplemented

    def dump(self):
        self._make()
        with self.fs.opendir(self.workdir) as d:
            with d.open(self.output, 'w') as fout:
                print(self.content, file=fout)


class ShellScriptMap(ShellScriptBase):
    def __init__(self, fs, workdir: str, output: str, tasks: list, shell='zsh'):
        super(__class__, self).__init__(fs, workdir, output, tasks, shell)
        self.task_type = 'map'
        self.commands = []

    def _add_if_gate(self, task):
        if task.get('method') == 'Gate':
            self.commands.append("Gate {}".format(task['filename']))

    def _add_if_root(self, task):
        if task['method'] == 'root':
            self.commands.append("root -q -b {}".format(task['filename']))

    def _get_workdir_on_local_and_server(self):
        from dxpy.filesystem import Path
        p_ser = self.fs.getsyspath(Path(self.workdir).abs)
        p_loc = (Path('~/Slurm/') / Path(self.workdir).rel).rel
        return p_ser, p_loc

    def _make(self):
        scrpt_tpl = self._load_shell_template()
        supported_tasks = [self._add_if_gate, self._add_if_root]
        for t in self.tasks:
            for add_if_func in supported_tasks:
                add_if_func(t)
        p_ser, p_loc = self._get_workdir_on_local_and_server()
        self.content = scrpt_tpl.render(local_work_directory=p_loc,
                                        server_work_directory=p_ser,
                                        commands='\n'.join(self.commands))


class ShellScriptMerge(ShellScriptBase):
    def __init__(self, fs, workdir: str, output: str, tasks: list, shell='zsh'):
        super(__class__, self).__init__(fs, workdir, output, tasks, shell)
        self.task_type = 'merge'

    def _make(self):
        scrpt_tpl = self._load_shell_template()
        self.content = scrpt_tpl.render(merge='merge' in self.tasks,
                                        clean='clean' in self.tasks)


class ShellScriptMaker:
    def __init__(self, fs, config):
        from .utils import sub_dir_filters
        self.fs = fs
        self.c = config['shell']
        self.sub_filters = sub_dir_filters(config)

    def make(self):
        from dxpy import batch
        sub_dirs = batch.DirectoriesFilter(self.sub_filters).lst(self.fs)
        for d in sub_dirs:
            ShellScriptMap(self.fs, d, self.c['map']['output'],
                           self.c['map']['tasks'], self.c['type']).dump()
        ShellScriptMerge(self.fs, '.', self.c['merge']['output'],
                         self.c['merge']['tasks'], self.c['type']).dump()


# class ShellScript:
#     def __init__(self, workdir=None, task_type='map', tasks=None, shell='zsh'):
#         self.workdir = workdir
#         if not task_type.lower() in ['map', 'merge']:
#             raise ValueError(
#                 "Task type {} is not supported.".format(task_type))
#         self.task_type = task_type.lower()
#         if not shell.lower() in ['bash', 'zsh']:
#             raise ValueError("Shell {} is not supported.".format(task_type))
#         self.shell = shell.lower()
#         self.tasks = tasks or []
#         self._make()

#     def dump(self):
#         if isinstance(self.output, str):
#             with OSFS('.') as fs:
#                 with fs.open(self.output, 'w') as fout:
#                     print('\n'.join(self.scripts), file=fout)
#         else:
#             print('\n'.join(self.scripts), file=self.output)

#     def add_head(self):
#         Snippets.add_shell(self.scripts, self.shell)
#         Snippets.add_sbatch(self.scripts)
#         Snippets.add_source(self.scripts, self.shell)
#         self.scripts.append('hostname')
#         self.scripts.append('date')

#     def add_tasks(self):
#         for t in self.tasks:
#             Snippets.add_task(self.scripts, t.get('name'), t.get('payloads'))

#     def add_tail(self):
#         self.scripts.append('date')
#         self.scripts.append('')
