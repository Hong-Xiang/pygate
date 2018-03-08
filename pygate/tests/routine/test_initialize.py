import unittest
from fs.memoryfs import MemoryFS
from dxl.fs import Directory
from pygate.routine.base import RoutineOnDirectory
from pygate.routine import initialize as ini


class TestSubdirectoriesMaker(unittest.TestCase):
    def test_dryrun(self):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o = ini.OpSubdirectoriesMaker(3)
        r = RoutineOnDirectory(d, [o], dryrun=True)
        result = o.dryrun(r)
        self.assertEqual(result[ini.KEYS.SUBDIRECTORIES],
                         ('sub.0', 'sub.1', 'sub.2'))

    def test_apply(self):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o = ini.OpSubdirectoriesMaker(3)
        r = RoutineOnDirectory(d, [o], dryrun=True)
        result = o.apply(r)
        dirs = ['sub.{}'.format(i) for i in range(3)]
        for d in dirs:
            self.assertTrue(mfs.exists(d))
