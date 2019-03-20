"""
"""
from .base import Operation, OperationOnFile, OperationOnSubdirectories, OpeartionWithShellCall, RoutineOnDirectory
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
    TO_BROADCAST_FILES = 'to_broadcast_files'


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


class OpGeneratorMac(OpGenerateFile, OpeartionWithShellCall):
    def __init__(self, script_filename: str, mac_config: str=None, mac_filename: str=None):
        super.__init__(filename)
        self.mac_config = mac_config
        self.mac_filename = mac_filename

    def call_args(self, r: RoutineOnDirectory):
        result = ['python', self.target(r).path.s]
        if self.mac_config is not None:
            result += ['--config', self.mac_config]
        if self.mac_filename is not None:
            result += ['--target', self.mac_filename]
        return result


class OpGenerateMacTemplate(OpGenerateFile):
    def __init__(self, filename):
        super().__init__(filename)
        from ..scripts.shell import ScriptMacTemplate
        self.script = ScriptMacTemplate()

    def content(self, r: RoutineOnDirectory) -> str:
        return self.script.render()


class OpGeneratorPhantom(OperationOnFile):
    def __init__(self, filename: str):
        super.__init__(filename)


