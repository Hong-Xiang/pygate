from .base import ObjectWithTemplate
import random
from typing import Tuple


class Script(ObjectWithTemplate):
    template = None


class Task:
    def render():
        raise NotImplementedError


class TaskWithFileArg(Task):
    def __init__(self, filename):
        self.fn = filename


class GateSimulation(TaskWithFileArg):
    def render(self):
        return "Gate {}".format(self.fn)


class RootAnalysis(TaskWithFileArg):
    def render(self):
        return "root -q -b {}".format(self.fn)


class Clean(Task):
    def render(self):
        return "pygate clean"


class Merge(Task):
    def render(self):
        return "pygate merge"


class ScriptRun(ObjectWithTemplate):
    template = 'run'

    def __init__(self, work_directory, tasks: Tuple[Task], geant4_version, shell='bash', is_need_source_env=False):
        self.work_directory = work_directory
        self.geant4_version = geant4_version
        self.shell = shell
        self.is_need_source_env = is_need_source_env
        self.tasks = tasks

    def add_task(self, task):
        return ScriptRun(self.work_directory, tuple(list(self.tasks) + [task]), self.geant4_version, self.shell, self.is_need_source_env)


class ScriptRunLocal(ScriptRun):
    template = 'run_local'

    def __init__(self, work_directory, tasks: Tuple[Task], geant4_version, shell='bash', is_need_source_env=False, local_work_directory=None):
        if local_work_directory is None:
            local_work_directory = '/tmp/pygate_temp_{}'.format(
                random.randint(0, 1e8))
        super().__init__(local_work_directory, tasks,
                         geant4_version, shell, is_need_source_env)
        self.server_work_directory = work_directory

    def add_task(self, task):
        return ScriptRunLocal(self.work_directory, tuple(list(self.tasks) + [task]), self.geant4_version, self.shell, self.is_need_source_env, self.local_work_directory)


class ScriptPostRun(Script):
    template = 'post_run'

    def __init__(self, tasks: Tuple[Task], shell='bash', is_need_source_env=False):
        self.tasks = tasks
        self.shell = shell
        self.is_need_source_env = is_need_source_env

    def add_task(self, task):
        return ScriptPostRun(tuple(list(self.tasks) + [task]), self.shell, self.is_need_source_env)
