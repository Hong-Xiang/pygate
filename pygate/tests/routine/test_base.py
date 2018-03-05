import unittest
from pygate.routine.base import Routine, Operation, RoutineOnDirectory


class TestRoutine(unittest.TestCase):
    def test_dryrun(self):
        class DummyOp(Operation):
            def apply(cls, x): return 'apply'

            def dryrun(cls, x): return 'dryrun'
        dummy_rout = Routine((DummyOp(), ), True)
        self.assertEqual(dummy_rout.work(), ('dryrun',))

    def test_apply(self):
        class DummyOp(Operation):
            def apply(cls, x): return 'apply'

            def dryrun(cls, x): return 'dryrun'
        dummy_rout = Routine((DummyOp(), ))
        self.assertEqual(dummy_rout.work(), ('apply',))


class TestRoutineOnDirectory(unittest.TestCase):
    def test_match(self):
        from fs.memoryfs import MemoryFS
        from dxl.fs import Directory
        mfs = MemoryFS()
        d = Directory('.', mfs)
        r = RoutineOnDirectory(d)
        for i in range(2):
            mfs.makedir('sub{}'.format(i))
        mfs.makedir('testdir')
        mfs.touch('sub.txt')
        sub_dirs = (r.list_matched_dirs(['sub*'])
                    .to_list().to_blocking().first())
        self.assertEqual(len(sub_dirs), 2)
        paths = [d.path.s for d in sub_dirs]
        self.assertIn('sub0', paths)
        self.assertIn('sub1', paths)
