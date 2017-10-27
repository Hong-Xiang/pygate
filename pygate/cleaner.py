class Cleaner:
    def __init__(self, fs, config):
        from .utils import sub_dir_filters
        self.fs = fs
        self.c = config['clean']
        self.sub_dir = sub_dir_filters(config)

    def clean(self):
        if self.c['sub_dirs']:
            self._clean_subs()
        if self.c['sources']:
            self._clean_sources()

    def msg(self, path):
        from fs.path import normpath
        if self.c['verbose'] > 0:
            print('DELETE: {}'.format(normpath(self.fs.getsyspath(path))))

    def _clean_subs(self):
        from dxpy.batch import DirectoriesFilter
        dirs = DirectoriesFilter(self.sub_dir).lst(self.fs)
        for d in dirs:
            self.msg(d)
            if not self.c['dryrun']:
                self.fs.removetree(d)

    def _clean_sources(self):
        from dxpy.batch import FilesFilter
        files = FilesFilter(['*']).lst(self.fs)
        for f in files:
            if f in self.c['keep']:
                continue
            self.msg(f)
            if not self.c['dryrun']:
                self.fs.remove(f)
