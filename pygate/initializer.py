"""
Initializer provide the following features:
    1. copy sources from template directory
    2. generate mac files
    3. generate sub directory structure
    4. copy sources/macs to sub directories
    5. generate map shell script to sub directories
    6. generate merge shell script in root directory

Grouped by two methods:
    1. pre_sub 1,2
    2. make_sub 3,4,5,6     
"""


class Initializer:
    def __init__(self, fs, config):
        self.fs = fs
        self.c = config['init']
        self.c_full = config

    def _copy_sources_from_template(self):
        from fs.path import relativefrom
        from fs.copy import copy_file
        from fs.osfs import OSFS
        path_source = self.c['source']['directory']
        if not path_source.startswith('/'):
            path_source = self.fs.getsyspath(path_source)
        with OSFS('/') as fs:
            if not fs.exists(path_source):
                raise ValueError(
                    "Source path {} not exists.".format(path_source))
        with OSFS(path_source) as fs_sor:

            for f in self.c['source']['filenames']:
                copy_file(fs_sor, f, self.fs, f)

    def _make_mac(self):
        from .template import MacMaker
        MacMaker.make_mac(self.c['generate']['config'])

    def _make_phantom(self):
        from .phantom import PhantomBinFileMaker
        PhantomBinFileMaker(self.fs, self.c['phantom']).make()

    def _sub_dir_name(self, i):
        return '{name}.{did}'.format(name=self.c_full['split']['name'], did=i)

    @property
    def _nb_sub_dirs(self):
        return self.c_full['split']['nb_split']

    def _make_subdirs(self):
        for i in range(self._nb_sub_dirs):
            self.fs.makedir(self._sub_dir_name(i), recreate=True)

    def _make_map_shell_scripts(self):
        from .shell import ShellScriptMaker
        ssm = ShellScriptMaker(self.fs, self.c_full)
        ssm.make()

    def _copy_sources_to_subdirs(self):
        from dxpy import batch
        from fs.copy import copy_file
        all_sources = batch.FilesFilter(['*']).lst(self.fs)
        for i in range(self._nb_sub_dirs):
            with self.fs.opendir(self._sub_dir_name(i)) as d:
                for f in all_sources:
                    copy_file(self.fs, f, d, f)

    def pre_sub(self):
        if 'source' in self.c:
            self._copy_sources_from_template()
        if 'generate' in self.c:
            self._make_mac()
        if 'phantom' in self.c:
            self._make_phantom()

    def make_sub(self):
        self._make_subdirs()
        self._copy_sources_to_subdirs()
        self._make_map_shell_scripts()
