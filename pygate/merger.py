class Merger:
    def __init__(self, fs, config):
        from .utils import sub_dir_filters
        self.fs = fs
        self.c = config['merge']
        self.sub_dirs = sub_dir_filters(config)

    def _path_of_file_in_sub_dirs(self, base_filename):
        from dxpy.batch import files_in_directories
        return files_in_directories(self.fs, self.sub_dirs, [base_filename])

    def msg(self, method, target, sources):
        if self.c.get('verbose') is not None and self.c['verbose'] > 0:
            print('MERGE.{md}.TARGET:'.format(md=method), target)
            print('MERGE.{md}.SOURCE:'.format(md=method), *sources, sep='\n')

    def _hadd(self, task):
        if not task['method'].lower() == 'hadd':
            return
        filename = task['filename']
        sub_filenames = self._path_of_file_in_sub_dirs(filename)
        path_target = self.fs.getsyspath(filename)
        path_filenames = [self.fs.getsyspath(f)
                          for f in sub_filenames if self.fs.exists(f)]
        call_args = ['hadd', path_target] + path_filenames
        self.msg('HADD', filename, sub_filenames)
        if not self.c['dryrun']:
            with subprocess.Popen(call_args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as p:
                sys.stdout.write(p.stdout.read().decode())
                sys.stderr.write(p.stderr.read().decode())

    def _cat(self, task):
        if not task['method'].lower() == 'cat':
            return
        target = task['filename']
        sources = self._path_of_file_in_sub_dirs(target)
        self.msg()
        if not self.c['dryrun']:
            with self.fs.open(target, 'w') as fout:
                for f in sources:
                    with self.fs.open(f) as fin:
                        print(fin.read(), end='', file=fout)

    def merge(self):
        supported_methods = [self._hadd, self._cat]
        for t in self.c['tasks']:
            for func in supported_methods:
                func(t)
