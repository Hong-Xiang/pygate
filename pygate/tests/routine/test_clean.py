import unittest
from pygate.routine.cleaner import OpCleanSource, OpCleanSubdirectories
from pygate.routine.base import RoutineOnDirectory
from dxl.fs import Directory
from fs.tempfs import TempFS


class TestCleanSource(unittest.TestCase):
    def test_dryrun(self):
        with TempFS() as tfs:
            tfs.touch('test.txt')
            tfs.touch('run.txt')
            o = OpCleanSource(['test.txt'])
            d = Directory('.', tfs)
            r = RoutineOnDirectory(d, [o])
            result = o.dryrun(r)
            self.assertEqual(result, {'remove': ['test.txt']})

    def test_apply(self):
        with TempFS() as tfs:
            tfs.touch('test.txt')
            tfs.touch('run.txt')
            self.assertTrue(tfs.exists('test.txt'))
            self.assertTrue(tfs.exists('run.txt'))
            o = OpCleanSource(['test.txt'])
            d = Directory('.', tfs)
            r = RoutineOnDirectory(d, [o])
            result = o.apply(r)
            self.assertFalse(tfs.exists('test.txt'))
            self.assertTrue(tfs.exists('run.txt'))

    def test_files(self):
        with TempFS() as tfs:
            tfs.touch('test.txt')
            tfs.touch('test1.txt')
            tfs.touch('test2.txt')
            tfs.touch('run.txt')
            o = OpCleanSource(['test*'])
            d = Directory('.', tfs)
            from dxl.fs import match_file
            r = RoutineOnDirectory(d, [o])
            files = (o.files(r).map(lambda f: f.path.s)
                     .to_list().to_blocking().first())
            self.assertEqual(sorted(files),
                             sorted(['test.txt', 'test1.txt', 'test2.txt']))


class TestCleanSubdirectories(unittest.TestCase):
    def test_apply(self):
        with TempFS() as tfs:
            tfs.makedir('sub0')
            tfs.makedir('sub1')
            tfs.makedir('run')
            self.assertTrue(tfs.exists('sub0'))
            self.assertTrue(tfs.exists('sub1'))
            self.assertTrue(tfs.exists('run'))
            o = OpCleanSubdirectories(['sub*'])
            d = Directory('.', tfs)
            r = RoutineOnDirectory(d, [o])
            result = o.apply(r)
            self.assertFalse(tfs.exists('sub0'))
            self.assertFalse(tfs.exists('sub1'))
            self.assertTrue(tfs.exists('run'))
