import unittest
from pygate.components.misc import *
from pygate.utils.strs import assert_equal_ignoring_multiple_whitespaces as ae

class TestDatabase(unittest.TestCase):
    def test_render(self):
        db = MaterialDatabaseLocal()
        ae(self, db.render(), "/gate/geometry/setMaterialDatabase    ./GateMaterials.db")