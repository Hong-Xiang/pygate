from .base import RoutineWithFS, Operation


class OpCleanSubdir(Operation):
    def get_dirs(self, r: RoutineWithFS):
        from dxpy.batch import DirectoriesFilter
        return DirectoriesFilter(['{}*'.format(r.split_name)]).lst(r.fs)

    def apply(self, r: RoutineWithFS):
        for d in self.get_dirs(r):
            r.fs.removetree(d)
        return self.dryrun(r)

    def dryrun(self, r: RoutineWithFS):
        return ['REMOVE: {}\n'.format(d) for d in self.get_dirs(r)]


class OpCleanSource(Operation):
    def get_sources(self, r: RoutineWithFS):
        from dxpy.batch import FilesFilter
        files = FilesFilter(['*']).lst(r.fs)


class Cleaner(RoutineWithFS):
    def __init__(self, fs, is_clean_subdir, is_clean_source, split_name, dryrun=False):
        ops = []
        if is_clean_subdir:
            ops.append(OpCleanSubdir())
        if is_clean_source:
            ops.append(OpCleanSource)
        super().__init__(fs, tuple(ops), dryrun)
        self.fs = fs
        self.split_name = split_name
        


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
