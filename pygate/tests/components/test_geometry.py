import unittest

from pygate.components.geometry import *


class TestVec3(unittest.TestCase):
    def test_render(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(v.render(), '1 2 3')


class TestVolume(unittest.TestCase):
    def test_render(self):
        # v = Volume('vol', 'Air', 'world', )
        pass


class TestBox(unittest.TestCase):
    def test_render(self):
        b = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        self.assertEqual(b.render(),
                         "/gate/world/geometry/setXLength         400.0 cm\n/gate/world/geometry/setYLength         400.0 cm\n/gate/world/geometry/setZLength         400.0 cm\n")


class TestCylinder(unittest.TestCase):
    def test_render(self):
        b = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        c = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                     mother='world', position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        self.assertEqual(c.render(),
                         '/gate/world/daughters/name            cylindricalPET\n/gate/world/daughters/insert          cylinder\n/gate/cylindricalPET/placement/setTranslation    0.0 0.0 0.0 cm\n/gate/cylindricalPET/geometry/setRmin         39.9 mm\n/gate/cylindricalPET/geometry/setRmax         52.0 mm\n/gate/cylindricalPET/geometry/setHeight         40.2 mm\n/gate/cylindricalPET/setMaterial                 Air\n')


class TestRepeatCubic(unittest.TestCase):
    def test_render(self):
        r = RepeaterCubic('crystal', Vec3(1, 5, 5, None), Vec3(0.0, 3.2, 4.0))
        self.assertEqual(r.render(),
                         '/gate/crystal/repeaters/insert          cubicArray\n/gate/crystal/cubicArray/setRepeatNumberX        1  \n/gate/crystal/cubicArray/setRepeatNumberY        5  \n/gate/crystal/cubicArray/setRepeatNumberZ        5  \n/gate/crystal/cubicArray/setRepeatVector         0.0 3.2 4.0 mm \n')
