from typing import Iterable, Dict, Any

from dxl.fs import Directory, File


class Operation:
    def apply(self, routine):
        raise NotImplementedError

    def dryrun(self, routine):
        raise NotImplementedError


class Routine:
    def __init__(self, operations: Iterable[Operation]=(),
                 dryrun=False, verbose=0):
        self.dryrun = dryrun
        self.ops = operations
        self.verbose = verbose
        self.result = []

    def last_result(self):
        if len(self.result) == 0:
            return {}
        return self.result[-1]

    def work(self):
        for o in self.ops:
            if self.dryrun:
                self.result.append(o.dryrun(self))
            else:
                self.result.append(o.apply(self))
        return tuple(self.result)

    def echo(self):
        import json
        return json.dumps(self.result, sort_keys=True, indent=4,
                          separators=(',', ': '))


class RoutineOnDirectory(Routine):
    def __init__(self,
                 directory: Directory,
                 operations: Iterable[Operation]=(),
                 dryrun=False, verbose=0):
        super().__init__(operations, dryrun, verbose)
        self.directory = directory

    # def list_matched_dirs(self, pattern):
    #     return (self.directory.listdir_as_observable()
    #             .filter(match_directory(pattern)))

    # def list_matched_files(self, pattern):
    #     from dxl.fs import match_file
    #     return (self.directory.listdir_as_observable()
    #             .filter(match_file(pattern)))

    # def list_files_in_dirs(self, sub_dir_pattern, filename):
    #     return self.list_matched_dirs().map(lambda d: d.attach(filename))


class OperationOnFile(Operation):
    """
    Methods:

    - `self.target(r: RoutineOnDirectory)`: Return corresponding File object.
    - `self.dryrun(r: RoutineOnDirectory)`: Return Dict['target', system path].
    """

    def __init__(self, filename: str):
        self.filename = filename

    def target(self, r: RoutineOnDirectory)-> File:
        return r.directory.attach_file(self.filename)

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        return {'target': self.target(r).path.s}

    def apply(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        return self.dryrun(r)


class OperationOnSubdirectories(Operation):
    def __init__(self, patterns: Iterable[str]):
        self.patterns = patterns

    def subdirectories(self, r: RoutineOnDirectory) -> 'Observable[Directory]':
        from dxl.fs import match_directory
        return (r.directory.listdir_as_observable()
                .filter(match_directory(self.patterns)))


class OpeartionWithShellCall(Operation):
    def call_args(self, r: Routine):
        raise NotImplementedError

    def stdout(self, r: Routine):
        return None

    def run_child_program(self, r: Routine):
        import subprocess
        import sys

        with subprocess.Popen(self.call_args(r),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True) as p:
            out = p.stdout.read().decode()
            err = p.stderr.read().decode()
            sys.stdout.write(out)
            sys.stderr.write(err)
        return {'out': out, 'err': err}

    def apply(self, r: Routine):
        result = self.dryrun(r)
        result.update(self.run_child_program(r))
        return result

    def dryrun(self, r: Routine) -> Dict[str, Iterable[str]]:
        return {'call_args': self.call_args(r)}
