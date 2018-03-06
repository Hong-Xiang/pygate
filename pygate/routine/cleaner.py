from dxl.fs import Directory, match_file
from .base import RoutineOnDirectory, OperationOnSubdirectories, Operation
from typing import Iterable


class OpCleanSubdirectories(OperationOnSubdirectories):
    def apply(self, r: RoutineOnDirectory):
        result = self.dryrun(r)
        (self.subdirectories(r).map(lambda d: d.remove())
         .to_list().to_blocking().first())
        return result

    def dryrun(self, r: RoutineOnDirectory):
        return {'remove': (self.subdirectories(r).map(lambda d: d.system_path())
                           .to_list().to_blocking().first())}


class OpCleanSource(Operation):
    def __init__(self, file_patterns: Iterable[str]):
        self.file_patterns = file_patterns

    def files(self, r: RoutineOnDirectory):
        return (r.directory.listdir_as_observable()
                .filter(match_file(self.file_patterns)))

    def apply(self, r: RoutineOnDirectory):
        result = self.dryrun(r)
        self.files(r).map(lambda f: f.remove()).to_list().to_blocking().first()
        return result

    def dryrun(self, r: RoutineOnDirectory):
        return {'remove': (self.files(r).map(lambda f: f.path.s)
                           .to_list().to_blocking().first())}


# class Cleaner(RoutineOnDirectory):
#     def __init__(self, , is_clean_subdir, is_clean_source, split_name, dryrun=False):
#         ops = []
#         if is_clean_subdir:
#             ops.append(OpCleanSubdir())
#         if is_clean_source:
#             ops.append(OpCleanSource)
#         super().__init__(fs, tuple(ops), dryrun)
#         self.fs = fs
#         self.split_name = split_name

    # def clean(self):
    #     if self.c['sub_dirs']:
    #         self._clean_subs()
    #     if self.c['sources']:
    #         self._clean_sources()

    # def msg(self, path):
    #     from fs.path import normpath
    #     if self.c['verbose'] > 0:
    #         print('DELETE: {}'.format(normpath(self.fs.getsyspath(path))))

    # def _clean_subs(self):
    #     from dxpy.batch import DirectoriesFilter
    #     dirs = DirectoriesFilter(self.sub_dir).lst(self.fs)
    #     for d in dirs:
    #         self.msg(d)
    #         if not self.c['dryrun']:
    #             self.fs.removetree(d)

    # def _clean_sources(self):
    #     from dxpy.batch import FilesFilter
    #     files = FilesFilter(['*']).lst(self.fs)
    #     for f in files:
    #         if f in self.c['keep']:
    #             continue
    #         self.msg(f)
    #         if not self.c['dryrun']:
    #             self.fs.remove(f)
