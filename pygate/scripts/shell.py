from .base import ObjectWithTemplate
import random
from typing import Tuple
from warnings import warn


class Script(ObjectWithTemplate):
    template = None

    def add_task(self, task):
        raise NotImplementedError


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
    def __init__(self, root_filename, c_file_name):
        super().__init__(root_filename)
        self.c_file_name = c_file_name

    def render(self):
        return "root -q -b {} {}".format(self.fn, self.c_file_name)


class PygateAnalysis(TaskWithFileArg):
    def __init__(self, source=None, target=None, output=None, name=None, analysis_type=None):
        super().__init__(target)
        self.source = source
        self.target = target
        self.output = output
        self.name = name
        self.analysis_type = analysis_type

    def render(self):
        if self.analysis_type == 'script':
            fmt = "pygate analysis script --source {} --target {} --output {}"
            return fmt.format(self.source, self.fn, self.output)
        elif self.analysis_type == 'predefined':
            fmt = "pygate analysis predefined --source {} --output {} --name {}"
            return fmt.format(self.source, self.output, self.name)
        else:
            raise ValueError("Unknown analysis subcommand {}.".format(self.analysis_type))


class Clean(Task):
    def render(self):
        return "pygate clean --subdirectories"


class Merge(TaskWithFileArg):
    def __init__(self, filename, method):
        super().__init__(filename)
        self.method = method

    def render(self):
        return "pygate merge --target {} --method {}".format(self.fn, self.method)


class ScriptRun(Script):
    template = 'run'

    def __init__(self, work_directory, tasks: Tuple[Task]=(), geant4_version='8.0', shell='bash', is_need_source_env=False, partition='cpu'):
        """
        Parameters:

        - is_need_source_env: switch whether add line `souce ~/.{shell}rc` to shell script generated.
        """
        self.work_directory = work_directory
        self.geant4_version = geant4_version
        self.shell = shell
        self.is_need_source_env = is_need_source_env
        self.tasks = tasks
        self.partition = partition

    def add_task(self, task):
        return ScriptRun(self.work_directory, tuple(list(self.tasks) + [task]), self.geant4_version, self.shell, self.is_need_source_env)


class ScriptRunLocal(ScriptRun):
    template = 'run_local'

    def __init__(self, work_directory, tasks: Tuple[Task], geant4_version, shell='bash', is_need_source_env=False, local_work_directory=None, partition='cpu'):
        if local_work_directory is None:
            local_work_directory = '/tmp/pygate_temp_{}'.format(
                random.randint(0, 1e8))
        super().__init__(local_work_directory, tasks,
                         geant4_version, shell, is_need_source_env)
        warn(DeprecationWarning("No local run script is needed when using gluster."))
        self.server_work_directory = work_directory
        self.partition = partition

    def add_task(self, task):
        return ScriptRunLocal(self.work_directory, tuple(list(self.tasks) + [task]), self.geant4_version, self.shell, self.is_need_source_env, self.local_work_directory)


class ScriptPostRun(Script):
    template = 'post_run'

    def __init__(self, tasks: Tuple[Task]=(), geant4_version='8.0', shell='bash', is_need_source_env=False, partition='cpu'):
        self.tasks = tasks
        self.shell = shell
        self.geant4_version = geant4_version
        self.is_need_source_env = is_need_source_env
        self.partition = partition

    def add_task(self, task):
        return ScriptPostRun(tuple(list(self.tasks) + [task]), self.shell, self.is_need_source_env)


class ScriptMacTemplate(ObjectWithTemplate):
    template = 'make_mac'
