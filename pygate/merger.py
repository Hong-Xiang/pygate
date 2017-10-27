from dxpy import batch


class Merger:
    def __init__(self, fs, config):
        self.fs = root_fs
        self.c = config['merge']
        self.c.update({'split': config['split']})

    def _path_of_file_in_sub_dirs(self, base_filename):
        return batch.files_in_directories([base_filename],
                                          [self.c['split'][name] + '*'])

    def _hadd(self, task):
        if not task['method'].lower() == 'hadd':
            return
        filename = task['filename']
        sub_filenames = self._path_of_file_in_sub_dirs(filename)
        path_target = fs.getsyspath(target)
        path_filenames = [fs.getsyspath(f) for f in filenames if fs.exists(f)]
        call_args = ['hadd', path_target] + path_filenames
        if self.c['dryrun']:
            print(' '.join(call_args))
        else:
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
        if self.c['dryrun']:
            print('MERGE.CAT.TARGET:', target)
            print('MERGE.CAT.SOURCE:\n', '\n'.join(sources))
        else:
            with fs.open(target, 'w') as fout:
                for f in sources:
                    with fs.open(f) as fin:
                        print(fin.read(), end='', file=fout)

    def merge(self):
        supported_methods = [self._hadd, self._cat]
        for t in self.c['tasks']:
            for func in supported_methods:
                func(t)
