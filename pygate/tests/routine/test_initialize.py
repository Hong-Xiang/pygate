import unittest
from unittest.mock import patch
from fs.memoryfs import MemoryFS
from dxl.fs import Directory, File
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


class TestOpGenerateFile(unittest.TestCase):
    @patch('pygate.routine.initialize.OpGenerateFile.content', return_value='test text')
    def test_dryrun(self, m):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o = ini.OpGenerateFile('test.txt')
        r = RoutineOnDirectory(d, [o])
        self.assertEqual(o.dryrun(r),
                         ini.TargetFileWithContent(File('test.txt', mfs),
                                                   content='test text').to_dict())

    @patch('pygate.routine.initialize.OpGenerateFile.content', return_value='test text')
    def test_apply(self, m):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o = ini.OpGenerateFile('test.txt')
        r = RoutineOnDirectory(d, [o])
        o.apply(r)
        with mfs.open('test.txt', 'r') as fin:
            result = fin.readlines()
        self.assertEqual(result, ['test text'])


class TestOpAddToBroadcastFile(unittest.TestCase):
    def test_dryrun(self):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o0 = ini.OpAddToBroadcastFile('test1.txt')
        o1 = ini.OpAddToBroadcastFile('test2.txt')
        r = RoutineOnDirectory(d, [o0, o1], dryrun=True)
        r.work()
        self.assertEqual(r.result[0], {ini.KEYS.TARGET: 'test1.txt',
                                       ini.KEYS.IS_TO_BROADCAST: True})
        self.assertEqual(r.result[1], {ini.KEYS.TARGET: 'test2.txt',
                                       ini.KEYS.IS_TO_BROADCAST: True})


class TestOpBroadcastFile(unittest.TestCase):
    @patch('pygate.routine.initialize.OpGenerateFile.content', return_value='test text')
    def test_files_to_broadcast(self, m):
        mfs = MemoryFS()
        d = Directory('.', mfs)
        o0 = ini.OpAddToBroadcastFile('test1.txt')
        o1 = ini.OpAddToBroadcastFile('test2.txt')
        o2 = ini.OpGenerateFile('test3.txt')
        o3 = ini.OpBroadcastFile(['sub*'])
        r = RoutineOnDirectory(d, [o0, o1, o2], dryrun=True)
        r.work()
        result = [f.path.s for f in o3.files_to_broadcast(r)]
        self.assertEqual(sorted(result),
                         sorted(['test{}.txt'.format(i) for i in range(1, 4)]))
