from typing import Tuple


class Operation:
    work_func = None
    msg_func = None

    def apply(self, routine):
        return self.work_func(routine)

    def dryrun(self, routine):
        return self.msg_func(routine)


class Routine:
    def __init__(self, operations: Tuple[Operation]=(), dryrun=False, verbose=0):
        self.dryrun = dryrun
        self.ops = operations
        self.verbose = verbose

    def work(self):
        result = []
        for o in self.ops:
            if self.dryrun:
                result.append(o.dryrun(self))
            else:
                result.append(o.apply(self))
        return tuple(result)
