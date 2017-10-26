from dxpy import batch
class Merger:
    def __init__(self, config, root_fs):
        """
        config: a dict of configurations:
            tasks: list of tasks:
                method: 'HADD' | 'CAT' | 'SUM'
                files: list of filenames
            dryrun: [OPTIONAL] bool
            target: [OPTIONAL] str, relative path of output directory
            verbose: [OPTIONAL] int
        """
        self.c = config
        self.fs = root_fs
        if 'dryrun' in self.c:
            self.dryrun = self.c['dryrun']
        else:
            self.dryrun = False
        self.target = self.get(['target']) or '.'
        self.verbose = self.get(['verbose']) or 1

    def func(self, name):
        return {
            'HADD': self.hadd,
            'CAT': self.cat,
            'SUM': self.sum
        }[name.upper()]

    def run(self):
        if not 'task' in self.c:
            return
        for task in self.c['tasks']:
            for fn in task['files']:
                self.func(task['method'])(fn)

    @classmethod
    def hadd(cls, filenames):
        path_target = fs.getsyspath(target)
        path_filenames = [fs.getsyspath(f) for f in filenames if fs.exists(f)]
        call_args = ['hadd', path_target] + path_filenames
        if dryrun:
            print(' '.join(call_args))
        else:
            with subprocess.Popen(call_args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as p:
                sys.stdout.write(p.stdout.read().decode())
                sys.stderr.write(p.stderr.read().decode())

    @classmethod
    def direct(cls, fs, target, filenames):
        with fs.open(targe, 'w') as fout:
            for f in filenames:
                with fs.open(f) as fin:
                    print(fin.read(), end='', file=fout)

    @classmethod
    def merge(cls, c):
        method = (c.get('merge') or {}).get('method') or 'DIRECT'
        files_to_merge = ((c.get('merge') or {}).get('filenames') or [])
        with OSFS(c['target']) as fs:
            for mfn in files_to_merge:
                filenames = []
                (methods.Mapper(fs).files(mfn)
                    .subscribe(filenames.append))
                if method.upper() == 'HADD':
                    cls.hadd(fs, mfn, filenames, c.get('dryrun'))
                elif method.upper() == 'DIRECT':
                    cls.direct(fs, mfn, filenames)
