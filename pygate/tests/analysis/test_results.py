import unittest
from pygate.analysis import results as rs


class TestResults(unittest.TestCase):
    def test_flatten(self):
        r = rs.Results((rs.Results([1, 2]),
                        rs.Results([3, 4]),
                        rs.Results([5, 6])))
        r = r.flatten()
        self.assertEqual(r.d, tuple(range(1, 7)))
