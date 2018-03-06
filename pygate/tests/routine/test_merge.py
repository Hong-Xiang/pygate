import unittest
from pygate.routine.merger import OpMerge, OpMergeHADD
from pygate.routine.base import RoutineOnDirectory
from typing import List


class TestMergeOperation(unittest.TestCase):
    def setUp(self):
        from fs.memoryfs import MemoryFS
        from dxl.fs import Directory
        import rx
        mfs = MemoryFS()
        d = Directory('.', mfs)
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        mfs.touch('test.txt')
        self.r = RoutineOnDirectory(d)
        self.o = OpMerge('test.txt', ['sub*'])

    def tearDown(self):
        self.r = None
        self.o = None

    def test_basic(self):
        subdirs: List[str] = (self.o.sources(self.r)
                              .map(lambda f: f.path.s)
                              .to_list().to_blocking().first())
        self.assertEqual(subdirs.sort(), [
                         'sub1/test.txt', 'sub2/test.txt'].sort())


class TestHadd(unittest.TestCase):
    def test_get_call_args(self):
        from fs.memoryfs import MemoryFS
        from dxl.fs import Directory
        import rx
        mfs = MemoryFS()
        d = Directory('.', mfs)
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        mfs.touch('test.txt')
        r = RoutineOnDirectory(d)
        o = OpMergeHADD('test.txt', ['sub*'])
        args = o.get_call_args(r)
        self.assertEqual(args[:2], ['hadd', 'test.txt'])
        self.assertEqual(args[2:].sort(),
                         ['sub1/test.txt', 'sub2/test.txt'].sort())

    def test_work(self):
        from fs.memoryfs import MemoryFS
        from dxl.fs import Directory
        from pygate.routine.base import RoutineOnDirectory
        from pygate.routine.merger import OpMerge, hadd
        import rx
        mfs = MemoryFS()
        d = Directory('.', mfs)
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        mfs.touch('test.txt')
        rh = hadd(d, ['sub*'], ['test.txt'], dryrun=True)
        result = rh.work()
        self.assertEqual(result[0]['merge_method'], 'hadd')
        
