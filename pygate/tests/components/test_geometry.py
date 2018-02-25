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

    def test_children(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44, 0, 0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head)
        crystal = Box('crystal', Vec3(30, 3, 3.8, 'mm'), 'Air', block)
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        self.assertEqual(world.render(),
                         '/gate/world/geometry/setXLength         400.0 cm\n/gate/world/geometry/setYLength         400.0 cm\n/gate/world/geometry/setZLength         400.0 cm\n\n/gate/world/daughters/name            cylindricalPET\n/gate/world/daughters/insert          cylinder\n/gate/cylindricalPET/placement/setTranslation    0.0 0.0 0.0 cm\n/gate/cylindricalPET/geometry/setRmin         39.9 mm\n/gate/cylindricalPET/geometry/setRmax         52.0 mm\n/gate/cylindricalPET/geometry/setHeight         40.2 mm\n/gate/cylindricalPET/setMaterial                 Air\n\n/gate/cylindricalPET/daughters/name            head\n/gate/cylindricalPET/daughters/insert          box\n/gate/head/placement/setTranslation    44 0 0 cm\n/gate/head/geometry/setXLength         8 cm\n/gate/head/geometry/setYLength         32 cm\n/gate/head/geometry/setZLength         40 cm\n/gate/head/setMaterial                 Air\n\n/gate/head/daughters/name            block\n/gate/head/daughters/insert          box\n/gate/block/geometry/setXLength         30 mm\n/gate/block/geometry/setYLength         16 mm\n/gate/block/geometry/setZLength         20 mm\n/gate/block/setMaterial                 Air\n\n/gate/block/daughters/name            crystal\n/gate/block/daughters/insert          box\n/gate/crystal/geometry/setXLength         30 mm\n/gate/crystal/geometry/setYLength         3 mm\n/gate/crystal/geometry/setZLength         3.8 mm\n/gate/crystal/setMaterial                 Air\n\n/gate/crystal/daughters/name            LSO\n/gate/crystal/daughters/insert          box\n/gate/LSO/placement/setTranslation    -0.75 0.0 0.0 cm\n/gate/LSO/geometry/setXLength         15 mm\n/gate/LSO/geometry/setYLength         3.0 mm\n/gate/LSO/geometry/setZLength         3.8 mm\n/gate/LSO/setMaterial                 LSO\n\n/gate/crystal/daughters/name            BGO\n/gate/crystal/daughters/insert          box\n/gate/BGO/placement/setTranslation    0.75 0.0 0.0 cm\n/gate/BGO/geometry/setXLength         15 mm\n/gate/BGO/geometry/setYLength         3.0 mm\n/gate/BGO/geometry/setZLength         3.8 mm\n/gate/BGO/setMaterial                 BGO\n')


class TestBox(unittest.TestCase):
    def test_render(self):
        b = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        self.assertEqual(b.render(),
                         "/gate/world/geometry/setXLength         400.0 cm\n/gate/world/geometry/setYLength         400.0 cm\n/gate/world/geometry/setZLength         400.0 cm\n")


class TestCylinder(unittest.TestCase):
    def test_render(self):
        b = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        c = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                     mother=b, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        self.assertEqual(c.render(),
                         '/gate/world/daughters/name            cylindricalPET\n/gate/world/daughters/insert          cylinder\n/gate/cylindricalPET/placement/setTranslation    0.0 0.0 0.0 cm\n/gate/cylindricalPET/geometry/setRmin         39.9 mm\n/gate/cylindricalPET/geometry/setRmax         52.0 mm\n/gate/cylindricalPET/geometry/setHeight         40.2 mm\n/gate/cylindricalPET/setMaterial                 Air\n')


class TestRepeatCubic(unittest.TestCase):
    def test_render(self):
        w = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        r = RepeaterCubic(Vec3(1, 5, 5, None), Vec3(0.0, 3.2, 4.0))
        c = Box('crystal', Vec3(10.0, 10.0, 10.0, 'mm'), 'Air', w, repeater=r)
        self.assertEqual(r.render(),
                         '/gate/crystal/repeaters/insert          cubicArray\n/gate/crystal/cubicArray/setRepeatNumberX        1  \n/gate/crystal/cubicArray/setRepeatNumberY        5  \n/gate/crystal/cubicArray/setRepeatNumberZ        5  \n/gate/crystal/cubicArray/setRepeatVector         0.0 3.2 4.0 mm \n')
