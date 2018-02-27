from typing import Tuple


class Operation:
    def __init__(self, work_func, msg_func):
        self.work_func = work_func
        self.msg_func = msg_func

    def apply(self, routine):
        return self.work_func(routine)

    def dryrun(self, routine):
        return self.msg_func(routine)


class Routine:
    def __init__(self, operations: Tuple[Operation]=(), dryrun=False):
        self.dryrun = dryrun
        self.ops = operations

    def work(self):
        result = []
        for o in self.ops:
            if self.dryrun:
                result.append(o.dryrun(self))
            else:
                result.append(o.apply(self))
        return tuple(result)
