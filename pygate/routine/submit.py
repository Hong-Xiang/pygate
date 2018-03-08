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

    def apply(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = self.dryrun(r)
        (self.subdirectories(r)
         .map(lambda d: submit_slurm(d, self.target(r)))
         .to_list().to_blocking().first())
        return result

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = (self.subdirectories(r)
                  .map(lambda d: {'work_directory': d.system_path(),
                                  'script_file': self.target(r).system_path()})
                  .to_list().to_blocking().first())
        return {'submitted': result}


class OpSubmitSingleFile(OperationOnFile):
    def __init__(self, filename: str, depens: Callable[[RoutineOnDirectory], Iterable[int]]):
        super().__init__(filename)
        self.depens = depens

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        result = {'depens': self.depens(r)}
