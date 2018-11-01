from .base import Operation, OperationOnFile, OperationOnSubdirectories
from dxl.fs import Directory, File
import os
from typing import Callable, Iterable, Dict, Any
from .base import RoutineOnDirectory
# from dxl.cluster import submit_slurm
# from dxl.cluster import Type, submit_task
# from dxl.cluster.backend import slurm

import requests

# TODO: Rework dicts to object, use ToSubmit Object replacing those dicts


class KEYS:
    SUBMITTED = 'Submitted'
    WORK_DIR = 'workdir'
    SCRIPT_FILE = 'script'
    SID = 'task_id'
    DEPENDENCIES = 'depends'
    # FATHER='father'


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
                result[k] = r[k].path.s
        for k in [KEYS.SID, KEYS.DEPENDENCIES]:
            if k in r:
                result[k] = r[k]
        return result
    except Exception as e:
        raise ValueError("Failed to parse paths from result {}.".format(r))


def submit_from_dict(r: Dict[str, Any], is_user_task=False) -> Dict[str, Any]:
    # print(f"print from routine/submit.submit_from_fict: {[r[KEYS.SCRIPT_FILE].path.s]}")
    # task = slurm.TaskSlurm(
    #                        # [r[KEYS.SCRIPT_FILE].path.s],
    #                        # workdir=r[KEYS.WORK_DIR].path.s,
    #                        details={"id": None,
    #                                 "worker": "cluster.sjtu.tech-pi.com",
    #                                 "workdir": str(r[KEYS.WORK_DIR].path.s),
    #                                 "depends": r.get(KEYS.DEPENDENCIES),
    #                                 "script": [r[KEYS.SCRIPT_FILE].path.s],
    #                                 "is_user_task": is_user_task},
    #                        # dependency=r.get(KEYS.DEPENDENCIES),
    #                        # is_root=True,
    #                        ttype=Type.Script)
    #
    # print("*************")
    # print(task)

    body = {
        'details': {
            "workdir": os.getcwd()+"/"+r[KEYS.WORK_DIR].path.s,
            "script": r[KEYS.SCRIPT_FILE].path.s,
            "is_user_task": is_user_task
        },
        "depends": r.get(KEYS.DEPENDENCIES, [])
    }
    print(body)
    sid = requests.post("http://localhost:23300/api/v1/tasks", json=body).json()['id']

    # sid = submit_task(task).id

    result = dict(r)
    result[KEYS.SID] = sid
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

    def to_submit(self, r: RoutineOnDirectory):
        submit_dict = {KEYS.WORK_DIR: r.directory,
                       KEYS.SCRIPT_FILE: self.target(r)}
        submit_dict[KEYS.DEPENDENCIES] = depens_from_result_dict(
            r.last_result()) 
        return submit_dict

    def apply(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        result = submit_from_dict(self.to_submit(r), True)
        return {KEYS.SUBMITTED: parse_paths_from_dict(result)}

    def dryrun(self, r: RoutineOnDirectory) -> Dict[str, Any]:
        return {KEYS.SUBMITTED: parse_paths_from_dict(self.to_submit(r))}
