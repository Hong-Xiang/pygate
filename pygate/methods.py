import rx
from fs.osfs import OSFS
from fs import path as fp
from fs import copy as fc


def files(fs, filters=None, walk=False, exclude_files=None):
    if filters is None:
        filters = []
    if exclude_files is None:
        exclude_files = []
    if walk:
        return (rx.Observable
                .from_(fs.walk.files('.', filter=filters))
                .map(lambda p: fp.relativefrom(fs.getsyspath('.'), p)))
    else:
        return rx.Observable.from_(fs.filterdir('.', files=filters, exclude_files=exclude_files, exclude_dirs=['*'])).map(lambda info: info.name)


def dirs(fs, filters=None, walk=False):
    if filters is None:
        filters = []
    if walk:
        return (rx.Observable
                .from_(fs.walk.dirs('.', filter=filters))
                .map(lambda p: fp.relativefrom(fs.getsyspath('.'), p)))
    else:
        return rx.Observable.from_(fs.filterdir('.', exclude_files=['*'], dirs=filters)).map(lambda info: info.name)


def make_subdirs(fs, prefix, nb_dirs):
    for i in range(nb_dirs):
        fs.mkdir('{0}.{1}'.format(prefix, i))


class Mapper:
    def __init__(self, fs, filters=None):
        self.fs = fs
        self.root = fp.normpath(self.fs.getsyspath('.'))
        if filters is None:
            filters = ['sub*']
        self.filters = filters

        self.subdirs = []
        dirs(self.fs, self.filters).subscribe(self.subdirs.append)

    def id_dir(self, path):
        if not fp.normpath(path) in self.subdirs:
            return None
        suffix = fp.splitext(path)
        return int(suffix[1:])

    def dirs(self):
        return rx.Observable.from_(self.subdirs)

    def subdirs_with_id(self):
        dir_with_id = [(d, self.id_dir(d)) for d in self.subdirs]
        return rx.Observable.from_(dir_with_id)

    def files(self, filename):
        return (self.dirs()
                .map(lambda d: fp.combine(d, filename)))
