"""
"""
from .base import Operation, OperationOnFile, OperationOnSubdirectories, RoutineOnDirectory
from dxl.fs import Directory, File
from typing import TypeVar, Iterable
from pygate.components.simulation import Simulation
from pygate.scripts.shell import Script
import rx


class KEYS:
    SUBDIRECTORIES = 'subdirectories'
    TARGET = 'target'
    IS_TO_BROADCAST = 'is_to_broadcast'
    CONTENT = 'content'


class TargetFileWithContent:
    def __init__(self, target: TypeVar('FileLike', File, str), is_to_broadcast: bool=True, content: str=None):
        if isinstance(target, File):
            self.target = target
        else:
            self.target = File(target)
        self.is_to_broadcast = is_to_broadcast
        self.content = content

    def to_dict(self):
        return {KEYS.TARGET: self.target.path.s,
                KEYS.IS_TO_BROADCAST: self.is_to_broadcast,
                KEYS.CONTENT: self.content}

    def save(self):
        if self.content is None:
            raise TypeError("None content to save.")
        self.target.save(self.content)


class OpAddToBroadcastFile(OperationOnFile):
    def __init__(self, filename):
        super().__init__(filename)

    def apply(self, r: RoutineOnDirectory):
        return self.dryrun(r)

    def dryrun(self, r: RoutineOnDirectory):
        return {KEYS.TARGET: self.target(r).path.s,
                KEYS.IS_TO_BROADCAST: True}


class OpGenerateFile(OperationOnFile):
    def __init__(self, filename: str, is_to_broadcast=True):
        super().__init__(filename)
        self.is_to_broadcast = is_to_broadcast

    def content(self, r: RoutineOnDirectory) -> str:
        raise NotImplementedError

    def target_file_with_content(self, r: RoutineOnDirectory):
        return TargetFileWithContent(self.target(r), self.is_to_broadcast,
                                     self.content(r))

    def apply(self, r: RoutineOnDirectory):
        f = self.target_file_with_content(r)
        f.save()
        return f.to_dict()

    def dryrun(self, r: RoutineOnDirectory):
        return self.target_file_with_content(r).to_dict()


class OpGeneratorMac(OpGenerateFile):
    def __init__(self, filename: str, simulation: Simulation):
        super.__init__(filename)
        self.simulation = simulation

    def content(self, r: RoutineOnDirectory)->str:
        return self.simulation.render()


class OpGeneratorShell(OperationOnFile):
    def __init__(self, filename: str, script: Script):
        super.__init__(filename)
        self.script = script

    def content(self, r: RoutineOnDirectory) -> str:
        return self.script.render()


class OpGeneratorPhantom(OperationOnFile):
    def __init__(self, filename: str):
        super.__init__(filename)


class OpSubdirectoriesMaker(Operation):
    def __init__(self, nb_split: int, subdirectory_format: str="sub.{}"):
        self.nb_split = nb_split
        self.fmt = subdirectory_format

    def apply(self, r: RoutineOnDirectory):
        result = self.dryrun(r)
        for n in result[KEYS.SUBDIRECTORIES]:
            r.directory.makedir(n)
        return result

    def dryrun(self, r: RoutineOnDirectory):
        return {KEYS.SUBDIRECTORIES: tuple([self.fmt.format(i) for i in range(self.nb_split)])}


class OpBroadcastFile(OperationOnSubdirectories):
    def files_to_broadcase(self, r: RoutineOnDirectory):
        result = []
        for res in r.result:
            if res.get(KEYS.IS_TO_BROADCAST, False):
                result.append(File(res[KEYS.TARGET], r.directory.filesystem))
        return result
    
    def dryrun(self, r:RoutineOnDirectory):
        pass
