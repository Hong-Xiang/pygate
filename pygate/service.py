from fs.osfs import OSFS
# from . import methods


from .template.service import MacMaker


# class EnsureFS:
#     def __init__(self, fs):
#         if isinstance(fs, str):
#             self.fs = OSFS(fs)
#             self.need_close = True
#         else:
#             self.fs = fs
#             self.need_close = False

#     def __enter__(self):
#         return self.fs

#     def __exit__(self, type, value, trackback):
#         if self.need_close:
#             self.fs.close()


# def copy_file(source, target, name):
#     """
#     Inputs:
#         source: directory, str or fs.baseFS
#         target: directory, str or fs.baseFS
#         name: filename, str
#     Raises:
#         None
#     Returns:
#         None
#     """
#     with EnsureFS(source) as fss, EnsureFS(target) as fst:
#         fc.copy_file(fss, name, fst, name)


# def copy_dir(source, target, filters=None):
#     with EnsureFS(source) as fss, EnsureFS(target) as fst:
#         filters = filters or ['*']
#         (methods.files(fss, filters)
#             .subscribe(lambda f: copy_file(fss, fst, f)))


# def copy_group(source, target, group_name):
#     with EnsureFS(source) as fss, EnsureFS(target) as fst:
#         with fss.opendir(group_name) as sd:
#             copy_dir(sd, fst)


def make_config(target='.'):
    from .config_maker import ConfigMaker
    from .config import config as c
    with OSFS('.') as fs:
        ConfigMaker.make(fs, '.')


def init(config, method):
    from .initializer import Initializer
    with OSFS('.') as fs:
        initer = Initializer(fs, config)
        if method == 'pre' or method == 'all':
            initer.pre_sub()
        if method == 'sub' or method == 'all':
            initer.make_sub()


def submit(config):
    from .submitter import Submitter
    with OSFS('.') as fs:
        Submitter(fs, config).submit()


def merge(config):
    from .merger import Merger
    with OSFS('.') as fs:
        Merger(fs, config).merge()


def clean(config):
    from .cleaner import Cleaner
    with OSFS('.') as fs:
        Cleaner(fs, config).clean()

# class Merger:
#     @classmethod
#     def hadd(cls, fs, target, filenames, dryrun=False):
#         path_target = fs.getsyspath(target)
#         path_filenames = [fs.getsyspath(f) for f in filenames if fs.exists(f)]
#         call_args = ['hadd', path_target] + path_filenames
#         if dryrun:
#             print(' '.join(call_args))
#         else:
#             with subprocess.Popen(call_args,
#                                   stdout=subprocess.PIPE,
#                                   stderr=subprocess.PIPE) as p:
#                 sys.stdout.write(p.stdout.read().decode())
#                 sys.stderr.write(p.stderr.read().decode())

#     @classmethod
#     def direct(cls, fs, target, filenames):
#         with fs.open(targe, 'w') as fout:
#             for f in filenames:
#                 with fs.open(f) as fin:
#                     print(fin.read(), end='', file=fout)

#     @classmethod
#     def merge(cls, c):
#         method = (c.get('merge') or {}).get('method') or 'DIRECT'
#         files_to_merge = ((c.get('merge') or {}).get('filenames') or [])
#         with OSFS(c['target']) as fs:
#             for mfn in files_to_merge:
#                 filenames = []
#                 (methods.Mapper(fs).files(mfn)
#                     .subscribe(filenames.append))
#                 if method.upper() == 'HADD':
#                     cls.hadd(fs, mfn, filenames, c.get('dryrun'))
#                 elif method.upper() == 'DIRECT':
#                     cls.direct(fs, mfn, filenames)
