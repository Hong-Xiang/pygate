import unittest
from pygate.routine.base import Routine, Operation, RoutineOnDirectory
from pygate.routine.base import OperationOnFile, OperationOnSubdirectories


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


class TestOperationOnSubdirectories(unittest.TestCase):
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
        o = OperationOnSubdirectories(['sub*'])
        sub_dirs = (o.subdirectories(r)
                    .to_list().to_blocking().first())
        self.assertEqual(len(sub_dirs), 2)
        paths = [d.path.s for d in sub_dirs]
        self.assertIn('sub0', paths)
        self.assertIn('sub1', paths)


class TestOperationOnFile(unittest.TestCase):
    def test_target(self):
        from fs.memoryfs import MemoryFS
        from dxl.fs import Directory
        from pygate.routine.base import RoutineOnDirectory
        from pygate.routine.merger import OpMerge
        import rx
        mfs = MemoryFS()
        d = Directory('.', mfs)
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        mfs.touch('test.txt')
        r = RoutineOnDirectory(d)
        o = OperationOnFile('test.txt')
        self.assertEqual(o.target(r).path.s, 'test.txt')
