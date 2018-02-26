import unittest
from pygate.utils.strs import assert_equal_ignoring_multiple_whitespaces as ae
from pygate.components.camera import Camera
from pygate.components.geometry import *


class TestCamera(unittest.TestCase):
    maxDiff = None

    def test_sd(self):
        from pygate.components.system import CylindericalPET
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
