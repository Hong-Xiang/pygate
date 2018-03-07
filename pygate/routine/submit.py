from .base import Operation
from .base import OperationOnFile


class OpSubmit(Operation):
    def to_submit(self):
        pass

    def dependencies(self):
        pass
    
    def dryrun(self):
        return {
            'to_submit': self.to_submit()
        }


class OpSubmitPreRun(Operation):
    def __init__(self):
        pass
