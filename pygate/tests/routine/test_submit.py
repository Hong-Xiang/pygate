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
        self.assertEqual(result['submitted'],
                         [{'work_directory': 'sub1',
                           'script_file': 'run.sh'},
                          {'work_directory': 'sub2',
                           'script_file': 'run.sh'}, ])
