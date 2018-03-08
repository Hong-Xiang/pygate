import unittest

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

# class TestSubmitSingleFile(unittest.TestCase):
#     def test_parse_depens(self):
#         mfs = MemoryFS()
#         mfs.touch('run.sh')
#         mfs.touch('post.sh')
#         mfs.makedir('sub1')
#         mfs.makedir('sub2')
#         d = Directory('.', mfs)
#         f = File('run.sh', mfs)
#         fp = File('post.sh', mfs)
#         op = submit.OpSubmitBroadcast('run.sh', ['sub*'])
#         r = submit.RoutineOnDirectory(d, [op])
#         result = op.dryrun(r)
#         self.assertEqual(result['submitted'],
#                          [{submit.KEYS.WORK_DIR: 'sub1',
#                            submit.KEYS.SCRIPT_FILE: 'run.sh'},
#                           {submit.KEYS.WORK_DIR: 'sub2',
#                            submit.KEYS.SCRIPT_FILE: 'run.sh'}, ])
