import unittest
from pygate.routine.base import Routine, Operation


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
