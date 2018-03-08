"""
"""
from .base import OperationOnFile, Operation


class OpGenerateFile(OperationOnFile):
    def __init__(self, filename: str):
        super().__init__(filename)

    def content(self):
        pass


class OpGeneratorMac(OpGenerateFile):
    def __init__(self, filename: str):
        super.__init__(filename)


class OpGeneratorShell(OperationOnFile):
    def __init__(self, filename: str):
        super.__init__(filename)


class OpGeneratorPhantom(OperationOnFile):
    def __init__(self, filename: str):
        super.__init__(filename)


class OpSubdirectoriesMaker(Operation):
    pass


class OpBroadcastFile(OperationOnFile):
    pass


class OpCopySharedFile(OperationOnFile):
    pass
