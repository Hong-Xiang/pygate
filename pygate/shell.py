class ShellScriptBase:
    def __init__(self, fs, workdir: str, output: str, tasks: list, shell='zsh', version='7.2'):
        self.fs = fs
        self.workdir = workdir
        self.output = output
        self.tasks = tasks
        self.shell = shell.lower()
        if not self.shell in ['zsh', 'bash']:
            raise ValueError("Unknown shell {}.".format(self.shell))
        self.content = None
        self.task_type = None
        self.version = version

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
    def __init__(self, fs, workdir: str, output: str, tasks: list, shell='zsh', version="7.2"):
        super(__class__, self).__init__(fs, workdir, output, tasks, shell, version)
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
        import os
        p_ser = self.fs.getsyspath(str(self.workdir))
        import random
        temps = random.randint(0, 100000000)
        subd = 'tmp{}'.format(temps)
        p_loc = Path('/tmp') / subd
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
                                        commands='\n'.join(self.commands),
                                        version=self.version)


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
        self.c['version'] = config['version']
        self.sub_filters = sub_dir_filters(config)

    def make(self):
        from dxpy import batch
        sub_dirs = batch.DirectoriesFilter(self.sub_filters).lst(self.fs)
        for d in sub_dirs:
            ShellScriptMap(self.fs, d, self.c['map']['output'],
                           self.c['map']['tasks'], self.c['type'], self.c['version']).dump()
        ShellScriptMerge(self.fs, '.', self.c['merge']['output'],
                         self.c['merge']['tasks'], self.c['type']).dump()
