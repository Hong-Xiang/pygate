from .base import Operation, OperationOnFile, OperationOnSubdirectories
from dxl.fs import Directory, File
from typing import Callable, Iterable, Dict, Any
from .base import RoutineOnDirectory
from dxl.cluster import submit_slurm


class OpSubmit(Operation):
    def to_submit(self):
        pass

    def dependencies(self):
        pass

    def dryrun(self):
        return {
            'to_submit': self.to_submit()
        }


class OpSubmitBroadcast(OperationOnSubdirectories, OperationOnFile):
    """
    Submit all files with given filename in subdirectories.
    """

    def __init__(self, filename, subdirectory_patterns: Iterable[str]):
        OperationOnSubdirectories.__init__(self, subdirectory_patterns)
        OperationOnFile.__init__(self, filename)

    def to_submit(self, r: RoutineOnDirectory) -> 'Observable[Dict[str, Any]]':
        return (self.subdirectories(r)
                .map(lambda d: {'work_directory': d,
                                'script_file': self.target(r)}))

    def apply(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = self.dryrun(r)
        (self.to_submit(r)
         .map(lambda dct: {'sid': submit_slurm(dct['work_directory'],
                                               dct['script_file']),
                           'work_dicectory': dct['work_directory'].system_path(),
                           'script_file': dct['script_file'].system_path()})
         .to_list().to_blocking().first())
        return result

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = (self.to_submit(r)
                  .map(lambda dct: {k: v.system_path() for k, v in dct.items()})
                  .to_list().to_blocking().first())
        return {'submitted': result}


class OpSubmitSingleFile(OperationOnFile):
    def __init__(self, filename: str, depens: Callable[[RoutineOnDirectory], Iterable[int]]):
        super().__init__(filename)
        self.depens = depens

    def parse_depens(self):
        pass

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        result = {'depens': self.depens(r)}
