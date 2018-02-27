import unittest
from pygate.routine.base import Routine, Operation
class TestRoutine(unittest.TestCase):
    def test_dryrun(self):
        dummy_op = Operation(lambda x: 'apply', lambda x: 'dryrun')
        dummy_rout = Routine((dummy_op, ), True)
        self.assertEqual(dummy_rout.work(), ('dryrun',))
    
    def test_apply(self):
        dummy_op = Operation(lambda x: 'apply', lambda x: 'dryrun')
        dummy_rout = Routine((dummy_op, ))
        self.assertEqual(dummy_rout.work(), ('apply',))