import unittest
from pygate.routine.merger import OpMerge
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
        self.o = OpMerge(['sub*'], ['test.txt'])

    def tearDown(self):
        self.r = None
        self.o = None

    def test_basic(self):
        subdirs: List[str] = (self.o.sub_dirs(self.r)
                              .map(lambda d: d.path.s)
                              .to_list().to_blocking().first())
        self.assertEqual(subdirs.sort(), ['sub1', 'su2'].sort())
