import unittest

from pygate.components.geometry import *
from pygate.utils.strs import assert_equal_ignoring_multiple_whitespaces as ae


class TestVec3(unittest.TestCase):
    def test_render(self):
        v = Vec3(1, 2, 3)
        ae(self, v.render(), '1 2 3')

    def test_render_unit(self):
        v = Vec3(0.0, 0.0, 0.0, 'mm')
        ae(self, v.render(), '0.0 0.0 0.0 mm')


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
    maxDiff = None

    def test_render(self):
        w = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        r = RepeaterCubic(Vec3(1, 5, 5, None), Vec3(0.0, 3.2, 4.0, 'mm'))
        c = Box('crystal', Vec3(10.0, 10.0, 10.0, 'mm'),
                'Air', w, repeaters=[r])
        ae(self, r.render(),
           '/gate/crystal/repeaters/insert          cubicArray\n/gate/crystal/cubicArray/setRepeatNumberX        1  \n/gate/crystal/cubicArray/setRepeatNumberY        5  \n/gate/crystal/cubicArray/setRepeatNumberZ        5  \n/gate/crystal/cubicArray/setRepeatVector         0.0 3.2 4.0 mm \n')

    def test_render_multiple(self):
        w = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        ecat = Cylinder('ecat', 442.0, 412.0, 155.2, material='Air', mother=w)
        r1 = RepeaterLinear(4, Vec3(0.0, 0.0, 38.8, 'mm'))
        r2 = RepeaterRing(72)
        block = Box('block', Vec3(30.0, 35.8594, 38.7), 'Air', position=Vec3(
            427.0, 0.0, 0.0, 'mm'), mother=ecat, repeaters=[r1, r2])
        rc = RepeaterCubic(Vec3(1, 8, 8), Vec3(0.0, 4.4942, 4.85, 'mm'))
        crystal = Box('crystal', Vec3(30.0, 4.4, 4.75),
                      'BGO', mother=block, repeaters=[rc])
        ae(self, w.render(),
           '/gate/world/geometry/setXLength 400.0 cm\n/gate/world/geometry/setYLength 400.0 cm\n/gate/world/geometry/setZLength 400.0 cm\n/gate/world/daughters/name ecat\n/gate/world/daughters/insert cylinder\n/gate/ecat/geometry/setRmin 412.0 mm\n/gate/ecat/geometry/setRmax 442.0 mm\n/gate/ecat/geometry/setHeight 155.2 mm\n/gate/ecat/setMaterial Air\n/gate/ecat/daughters/name block\n/gate/ecat/daughters/insert box\n/gate/block/placement/setTranslation 427.0 0.0 0.0 mm\n/gate/block/geometry/setXLength 30.0 mm\n/gate/block/geometry/setYLength 35.8594 mm\n/gate/block/geometry/setZLength 38.7 mm\n/gate/block/setMaterial Air\n/gate/block/daughters/name crystal\n/gate/block/daughters/insert box\n/gate/crystal/geometry/setXLength 30.0 mm\n/gate/crystal/geometry/setYLength 4.4 mm\n/gate/crystal/geometry/setZLength 4.75 mm\n/gate/crystal/setMaterial BGO\n/gate/crystal/repeaters/insert cubicArray\n/gate/crystal/cubicArray/setRepeatNumberX 1\n/gate/crystal/cubicArray/setRepeatNumberY 8\n/gate/crystal/cubicArray/setRepeatNumberZ 8\n/gate/crystal/cubicArray/setRepeatVector 0.0 4.4942 4.85 mm\n/gate/block/repeaters/insert linear\n/gate/block/linear/setRepeatNumber 4\n/gate/block/linear/setRepeatVector 0.0 0.0 38.8 mm\n/gate/block/repeaters/insert ring\n/gate/block/ring/setRepeatNumber 72')


class TestSurface(unittest.TestCase):
    def test_render_perfect_apd(self):
        class DummyVolume:
            def __init__(self, name):
                self.name = name
        crystal = DummyVolume('crystal')
        elec = DummyVolume('Electronics')
        s = SurfacePerfectAPD('Detection1', crystal, elec)
        ae(self, s.render(),
           '/gate/crystal/surfaces/name                           Detection1\n/gate/crystal/surfaces/insert                         Electronics\n/gate/crystal/surfaces/Detection1/setSurface          perfect_apd ')


class TestPhantom(unittest.TestCase):
    def test_render(self):
        class DummyVolume:
            name = 'phantom'
        p = Phantom((DummyVolume,))
        self.assertEqual(p.render(),
                         '/gate/phantom/attachPhantomSD\n')


class TestCamera(unittest.TestCase):
    maxDiff = None

    def test_sd(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 520.0, 399.0, 402.0, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        rh = RepeaterRing(4)
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44.0, 0.0, 0.0, 'cm'), repeaters=[rh])
        rb = RepeaterCubic(Vec3(1, 20, 20), Vec3(0.0, 1.6, 2.0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head,
                    position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rb])
        rc = RepeaterCubic(Vec3(1, 5, 5), Vec3(0.0, 3.2, 4.0, 'mm'))
        crystal = Box('crystal', Vec3(30, 3.0, 3.8, 'mm'), 'Air',
                      block, position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rc])
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        system = CylindericalPET(head, block, crystal=crystal,
                                 layer0=lso, layer1=bgo)
        camera = Camera(system, [lso, bgo])
        ae(self, camera.render(),
           '/gate/systems/cylindricalPET/rsector/attach head\n/gate/systems/cylindricalPET/module/attach block\n/gate/systems/cylindricalPET/crystal/attach crystal\n/gate/systems/cylindricalPET/layer0/attach LSO\n/gate/systems/cylindricalPET/layer1/attach BGO\n/gate/LSO/attachCrystalSD\n/gate/BGO/attachCrystalSD')


class TestCylindrical(unittest.TestCase):
    def test_render(self):
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
        system = CylindericalPET(
            head, block, crystal=crystal, layer0=lso, layer1=bgo)
        self.assertEqual(system.render(),
                         '/gate/systems/cylindricalPET/rsector/attach   head\n/gate/systems/cylindricalPET/module/attach   block\n/gate/systems/cylindricalPET/crystal/attach   crystal\n/gate/systems/cylindricalPET/layer0/attach   LSO\n/gate/systems/cylindricalPET/layer1/attach   BGO\n')


class TestGeometry(unittest.TestCase):
    def test_render(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 520.0, 399.0, 402.0, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        rh = RepeaterRing(4)
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44.0, 0.0, 0.0, 'cm'), repeaters=[rh])
        rb = RepeaterCubic(Vec3(1, 20, 20), Vec3(0.0, 1.6, 2.0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head,
                    position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rb])
        rc = RepeaterCubic(Vec3(1, 5, 5), Vec3(0.0, 3.2, 4.0, 'mm'))
        crystal = Box('crystal', Vec3(30, 3.0, 3.8, 'mm'), 'Air',
                      block, position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rc])
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        system = CylindericalPET(head, block, crystal=crystal,
                                 layer0=lso, layer1=bgo)
        camera = Camera(system, [lso, bgo])
        casper = Box('casper', Vec3(50.0, 50.0, 17.0, 'mm'), 'RhB', world)
        phantom = Phantom((casper,))

        surfaces = (SurfacePerfectAPD('Detection1', block, crystal),)
        geometry = Geometry(world, camera, phantom, surfaces)
