import unittest
from unittest.mock import patch, Mock
from fs.memoryfs import MemoryFS
from dxl.fs import Directory, File
from pygate.routine import submit


class TestSubmitBroadcast(unittest.TestCase):
    def test_dryrun(self):
        mfs = MemoryFS()
        mfs.touch('run.sh')
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        d = Directory('.', mfs)
        f = File('run.sh', mfs)
        op = submit.OpSubmitBroadcast('run.sh', ['sub*'])
        r = submit.RoutineOnDirectory(d, [op])
        result = op.dryrun(r)
        self.assertEqual(result[submit.KEYS.SUBMITTED],
                         [{submit.KEYS.WORK_DIR: 'sub1',
                           submit.KEYS.SCRIPT_FILE: 'run.sh'},
                          {submit.KEYS.WORK_DIR: 'sub2',
                           submit.KEYS.SCRIPT_FILE: 'run.sh'}, ])

    def test_dryrun_last_result(self):
        mfs = MemoryFS()
        mfs.touch('run.sh')
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        d = Directory('.', mfs)
        f = File('run.sh', mfs)
        op = submit.OpSubmitBroadcast('run.sh', ['sub*'])
        r = submit.RoutineOnDirectory(d, [op], dryrun=True)
        r.work()
        self.assertEqual(r.last_result()[submit.KEYS.SUBMITTED],
                         [{submit.KEYS.WORK_DIR: 'sub1',
                           submit.KEYS.SCRIPT_FILE: 'run.sh'},
                          {submit.KEYS.WORK_DIR: 'sub2',
                           submit.KEYS.SCRIPT_FILE: 'run.sh'}, ])

    # @patch('dxl.cluster.submit_slurm', side_effect=[111, 112])
    # def test_submit_from_dict(self):

# m = Mock(side_effect=[111, 112])


class TestSubmitSingleFile(unittest.TestCase):
    @patch('pygate.routine.submit.submit_slurm', side_effect=[111, 112])
    def test_parse_depens(self, m):
        mfs = MemoryFS()
        mfs.touch('run.sh')
        mfs.touch('post.sh')
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        d = Directory('.', mfs)
        f = File('run.sh', mfs)
        fp = File('post.sh', mfs)
        op = submit.OpSubmitBroadcast('run.sh', ['sub*'])
        r = submit.RoutineOnDirectory(d, [op])
        result = op.apply(r)
        depens = submit.depens_from_result_dict(result)
        self.assertEqual(sorted(depens), sorted([111, 112]))

    @patch('pygate.routine.submit.depens_from_result_dict', return_value=[111, 112])
    def test_dryrun(self, m):
        mfs = MemoryFS()
        mfs.touch('run.sh')
        mfs.touch('post.sh')
        mfs.makedir('sub1')
        mfs.makedir('sub2')
        d = Directory('.', mfs)
        f = File('run.sh', mfs)
        fp = File('post.sh', mfs)
        op = submit.OpSubmitSingleFile('post.sh')
        r = submit.RoutineOnDirectory(d, [op])
        result = op.dryrun(r)
        self.assertEqual(result[submit.KEYS.SUBMITTED],
                         {submit.KEYS.WORK_DIR: '',
                          submit.KEYS.SCRIPT_FILE: 'post.sh',
                          submit.KEYS.DEPENDENCIES: [111, 112]})
