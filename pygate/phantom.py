class PhantomBinFileMaker:
    def __init__(self, fs, phantom_files):
        self.fs = fs
        self.phantom_files = phantom_files

    def _load_data(self, source):
        from dxpy.filesystem import Path
        import numpy as np
        from scipy.io import loadmat
        source = Path(source)
        source_syspath = self.fs.getsyspath(str(source))
        if source.suffix == '.npy':
            data = np.load(source_syspath)
            data = data.T
        else:
            data_dct = loadmat(source_syspath)
            data = data_dct[data_dct.keys()[0]]
        return data

    def _make_bin(self, target, data):
        with self.fs.open(target, 'wb') as fout:
            fout.write(data.tostring())

    def make(self):
        for s, t in self.phantom_files:
            self._make_bin(t, self._load_data(s))
