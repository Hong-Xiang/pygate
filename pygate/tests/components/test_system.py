import unittest
from pygate.components.system import *
from pygate.components.geometry import *


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

 