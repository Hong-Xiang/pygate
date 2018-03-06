from .base import RoutineOnDirectory, OperationOnFile, OperationOnSubdirectories, OpeartionWithShellCall
from dxl.fs import Path, File, Directory
from ..utils.typing import JSONStr
import json

from rx import Observable
from typing import Iterable, Callable
from functools import partial


class OpMerge(OperationOnFile, OperationOnSubdirectories):
    method = 'dryrun'

    def __init__(self, filename: str, patterns: Iterable[str]):
        OperationOnFile.__init__(self, filename)
        OperationOnSubdirectories.__init__(self, patterns)

    def sources(self, r: RoutineOnDirectory):
        return self.subdirectories(r).map(lambda d: d.attach_file(self.filename))

    def dryrun(self, r: RoutineOnDirectory):
        sources_system_path = (self.sources(r)
                               .map(lambda f: f.system_path())
                               .to_list().to_blocking().first())
        result = {
            'merge_method': self.method,
            'sources': sources_system_path,
        }
        result.update(OperationOnFile.dryrun(self, r))
        return result


# class RoutineMerge(RoutineOnDirectory):
#     def __init__(self, directory: Directory, operations: Iterable[Operation]=(), dryrun=False, verbose=0):
#         super().__init__(directory, operations, dryrun, verbose)

#         # class OpMergeMultipleFile(Operation):
#         #     def __init__(self, filename_patterns, subdir_pattern, op: OpMergeSingleFile):
#         #         self.fns = filename_patterns
#         #         self.sds = subdir_pattern
#         #         self.op = op

#         #     def get_sub_ops(self, r: RoutineOnDirectory):
#         #         return (r.list_matched_files(self.fns)
#         #                 .map(lambda f: self.op(f, self.sds)))

#         #     def apply(self, r: RoutineOnDirectory):
#         #         return (self.get_sub_ops(r)
#         #                 .map(lambda o: o.apply(r))
#         #                 .to_list().to_blocking.first())

#         #     def dryrun(self, r: RoutineOnDirectory):
#         #         return (self.get_sub_ops(r)
#         #                 .map(lambda o: o.dryrun(r))
#         #                 .to_list().to_blocking.first())


class OpMergeHADD(OpMerge, OpeartionWithShellCall):
    method = 'hadd'

    def __init__(self, filename: str, patterns: Iterable[str]):
        OpMerge.__init__(self, filename, patterns)

    def call_args(self, r: RoutineOnDirectory):
        target = self.target(r).system_path()
        sources = (self.sources(r)
                   .map(lambda f: f.system_path())
                   .to_list().to_blocking().first())
        call_args = ['hadd', target] + sources
        return call_args

    def dryrun(self, r: RoutineOnDirectory):
        result = OpMerge.dryrun(self, r)
        result.update(OpeartionWithShellCall.dryrun(self, r))
        return result


class OpMergeCat(OpMerge):
    method = 'cat'


class OpMergeSumBinary(OpMerge):
    method = 'sum_bin'


def hadd(work_directory: Directory, subdirectory: str, source_filenames: Iterable[str], dryrun=False):
    ops = [OpMergeHADD(s, subdirectory) for s in source_filenames]
    return RoutineOnDirectory(work_directory, ops, dryrun)
    # class OpMergeCat(Operation):
    #     method = 'cat'
    #     def apply(self, r:RoutineOnDirectory):

    #     with self.fs.open(target, 'w') as fout:
    #                 for f in sources:
    #                     with self.fs.open(f) as fin:
    #                         print(fin.read(), end='', file=fout

    # class OpMergeSum(Operation):
    #     def __init__(self, dtype, sources, target):
    #         super().__init__(sources, target)
    #         self.dtype = dtype

    # class OpMergeCopy(Operation):
    #     pass

    # class Merger:
    #     def __init__(self, fs, config):
    #         from .utils import sub_dir_filters
    #         self.fs = fs
    #         self.c = config['merge']
    #         self.sub_dirs = sub_dir_filters(config)

    #     def _path_of_file_in_sub_dirs(self, base_filename):
    #         from dxpy.batch import files_in_directories
    #         return files_in_directories(self.fs, self.sub_dirs, [base_filename])

    #     def msg(self, method, target, sources):
    #         if self.c.get('verbose') is not None and self.c['verbose'] > 0:
    #             print('MERGE.{md}.TARGET:'.format(md=method), target)
    #             print('MERGE.{md}.SOURCE:'.format(md=method), *sources, sep='\n')

    #     def _hadd(self, task):
    #         import subprocess
    #         import sys
    #         if not task['method'].lower() == 'hadd':
    #             return
    #         filename = task['filename']
    #         sub_filenames = self._path_of_file_in_sub_dirs(filename)
    #         path_target = self.fs.getsyspath(filename)
    #         path_filenames = [self.fs.getsyspath(f)
    #                           for f in sub_filenames if self.fs.exists(f)]
    #         call_args = ['hadd', path_target] + path_filenames
    #         self.msg('HADD', filename, sub_filenames)
    #         if not self.c['dryrun']:
    #             with subprocess.Popen(call_args,
    #                                   stdout=subprocess.PIPE,
    #                                   stderr=subprocess.PIPE) as p:
    #                 sys.stdout.write(p.stdout.read().decode())
    #                 sys.stderr.write(p.stderr.read().decode())

    #     def _cat(self, task):
    #         if not task['method'].lower() == 'cat':
    #             return
    #         target = task['filename']
    #         sources = self._path_of_file_in_sub_dirs(target)
    #         self.msg('cat', target, sources)
    #         if not self.c['dryrun']:
    #             )

    #     def _sum(self, task):
    #         import numpy as np
    #         if not task['method'].lower() == 'sum':
    #             return
    #         target = task['filename']
    #         sources = self._path_of_file_in_sub_dirs(target)
    #         self.msg('sum', target, sources)
    #         dtype = task['dtype']
    #         mapped = {
    #             'float32': np.float32,
    #             'uint16': np.uint16,
    #             'uint8': np.uint8,
    #         }
    #         dtype = mapped[dtype]
    #         result = None
    #         for f in sources:
    #             with self.fs.open(f, 'rb') as fin:
    #                 data = np.fromstring(fin.read(), dtype=dtype)
    #                 if result is None:
    #                     result = data
    #                 else:
    #                     result += data
    #         with self.fs.open(target, 'wb') as fout:
    #             fout.write(result.tostring())

    #     def _copy(self, task):
    #         import numpy as np
    #         if not task['method'].lower() == 'sum':
    #             return
    #         target = task['filename']
    #         sources = self._path_of_file_in_sub_dirs(target)
    #         if len(sources):
    #             raise ValueError("Sources not found")
    #         from fs.copy import copy_file
    #         self.msg('copy', target, sources[0])
    #         copy_file(self.fs, sources[0], self.fs, target)

    #     def merge(self):
    #         supported_methods = [self._hadd, self._cat, self._sum]
    #         for t in self.c['tasks']:
    #             for func in supported_methods:
    #                 func(t)
