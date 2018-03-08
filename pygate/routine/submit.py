from .base import Operation, OperationOnFile, OperationOnSubdirectories
from dxl.fs import Directory, File
from typing import Callable, Iterable, Dict, Any
from .base import RoutineOnDirectory
from dxl.cluster import submit_slurm


class KEYS:
    SUBMITTED = 'submitted'
    WORK_DIR = 'work_directory'
    SCRIPT_FILE = 'script_file'
    SID = 'sid'
    DEPENDENCIES = 'depens'


def depens_from_result_dict(r: Dict[str, Any]) -> Iterable[int]:
    try:
        result = []
        if KEYS.SUBMITTED in r:
            for t in r[KEYS.SUBMITTED]:
                if t.get(KEYS.SID) is not None:
                    result.append(int(t[KEYS.SID]))
        return result
    except Exception as e:
        raise ValueError("Failed to parse depens from result {}.".format(r))


def append_depens_to_dict(to_submit: Dict[str, Any], previous_result: Dict[str, Any]):
    result = dict(to_submit)
    result[KEYS.DEPENDENCIES] = depens_from_result(previous_result)
    return result


def parse_paths_from_dict(r: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = dict(r)
        for k in [KEYS.WORK_DIR, KEYS.SCRIPT_FILE]:
            if k in r:
                result[k] = r[k].system_path()
        if KEYS.SID in r:
            result[KEYS.SID] = r[KEYS.SID]
        return result
    except Exception as e:
        raise ValueError("Failed to parse paths from result {}.".format(r))


def submit_from_dict(r: Dict[str, Any]) -> Dict[str, Any]:
    sid = submit_slurm(r[KEYS.WORK_DIR],
                       r[KEYS.SCRIPT_FILE],
                       r.get(KEYS.DEPENDENCIES, ()))
    result = dict(r)
    r[KEYS.SID] = sid
    return result


class OpSubmitBroadcast(OperationOnSubdirectories, OperationOnFile):
    """
    Submit all files with given filename in subdirectories.
    """

    def __init__(self, filename, subdirectory_patterns: Iterable[str]):
        OperationOnSubdirectories.__init__(self, subdirectory_patterns)
        OperationOnFile.__init__(self, filename)

    def to_submit(self, r: RoutineOnDirectory) -> 'Observable[Dict[str, Any]]':
        return (self.subdirectories(r)
                .map(lambda d: {KEYS.WORK_DIR: d,
                                KEYS.SCRIPT_FILE: self.target(r)}))

    def apply(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = (self.to_submit(r)
                  .map(submit_from_dict)
                  .map(parse_paths_from_dict)
                  .to_list().to_blocking().first())
        return {KEYS.SUBMITTED: result}

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Iterable[Dict[str, str]]]:
        result = (self.to_submit(r)
                  .map(parse_paths_from_dict)
                  .to_list().to_blocking().first())
        return {KEYS.SUBMITTED: result}


class OpSubmitSingleFile(OperationOnFile):
    def __init__(self, filename: str):
        super().__init__(filename)

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        result = {'depens': self.depens(r)}
