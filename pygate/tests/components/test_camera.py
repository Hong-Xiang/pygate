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
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head, position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rb])
        rc = RepeaterCubic(Vec3(1, 5, 5), Vec3(0.0, 3.2, 4.0, 'mm'))
        crystal = Box('crystal', Vec3(30, 3.0, 3.8, 'mm'), 'Air', block, position=Vec3(0.0, 0.0, 0.0, 'cm'), repeaters=[rc])
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        system = CylindericalPET(head, block, crystal=crystal,
                                 layer0=lso, layer1=bgo)
        camera = Camera(world, system, [lso, bgo])
        ae(self, camera.render(),
           '#\n#     W O R L D\n#\n/gate/world/geometry/setXLength       400.0 cm\n/gate/world/geometry/setYLength       400.0 cm\n/gate/world/geometry/setZLength       400.0 cm\n\n\n#-------------------oooooOOOOO00000OOOOOooooo---------------------#\n#                                                                 #\n#     D E F I N I T I O N   A N D   D E S C R I T I O N           #\n#        O F   Y O U R   P E T   D E V I C E                      #\n#                                                                 #\n#-------------------oooooOOOOO00000OOOOOooooo---------------------#\n\n#	CYLINDRICAL\n/gate/world/daughters/name                    cylindricalPET\n/gate/world/daughters/insert                  cylinder\n/gate/cylindricalPET/placement/setTranslation 0.0 0.0 0.0 cm\n/gate/cylindricalPET/geometry/setRmin         399.0 mm\n/gate/cylindricalPET/geometry/setRmax         520.0 mm\n/gate/cylindricalPET/geometry/setHeight       402.0 mm\n/gate/cylindricalPET/setMaterial              Air\n\n#	HEAD\n/gate/cylindricalPET/daughters/name           head\n/gate/cylindricalPET/daughters/insert         box\n/gate/head/placement/setTranslation           44.0 0.0 0.0 cm\n/gate/head/geometry/setXLength                8  cm\n/gate/head/geometry/setYLength                32 cm\n/gate/head/geometry/setZLength                40 cm\n/gate/head/setMaterial                        Air\n\n\n#	BLOCK\n/gate/head/daughters/name                     block\n/gate/head/daughters/insert                   box\n/gate/block/placement/setTranslation          0.0 0.0 0.0 cm\n/gate/block/geometry/setXLength               30 mm\n/gate/block/geometry/setYLength               16 mm\n/gate/block/geometry/setZLength               20 mm\n/gate/block/setMaterial                       Air\n\n#	C R Y S T A L\n/gate/block/daughters/name                    crystal\n/gate/block/daughters/insert                  box\n/gate/crystal/placement/setTranslation        0.0 0.0 0.0 cm\n/gate/crystal/geometry/setXLength             30 mm\n/gate/crystal/geometry/setYLength             3.0 mm\n/gate/crystal/geometry/setZLength             3.8 mm\n/gate/crystal/setMaterial                     Air\n\n\n#	LSO layer\n/gate/crystal/daughters/name                  LSO\n/gate/crystal/daughters/insert                box\n/gate/LSO/placement/setTranslation            -0.75 0.0 0.0 cm\n/gate/LSO/geometry/setXLength                 15 mm\n/gate/LSO/geometry/setYLength                 3.0 mm\n/gate/LSO/geometry/setZLength                 3.8 mm\n/gate/LSO/setMaterial                         LSO\n\n#	BGO layer\n/gate/crystal/daughters/name                  BGO\n/gate/crystal/daughters/insert                box\n/gate/BGO/placement/setTranslation            0.75 0.0 0.0 cm\n/gate/BGO/geometry/setXLength                 15 mm\n/gate/BGO/geometry/setYLength                 3.0 mm\n/gate/BGO/geometry/setZLength                 3.8 mm\n/gate/BGO/setMaterial                         BGO\n#	R E P E A T    C R Y S T A L\n/gate/crystal/repeaters/insert                cubicArray\n/gate/crystal/cubicArray/setRepeatNumberX     1\n/gate/crystal/cubicArray/setRepeatNumberY     5\n/gate/crystal/cubicArray/setRepeatNumberZ     5\n/gate/crystal/cubicArray/setRepeatVector      0.0 3.2 4.0 mm\n\n\n#	R E P E A T    BLOCK\n/gate/block/repeaters/insert                  cubicArray\n/gate/block/cubicArray/setRepeatNumberX       1\n/gate/block/cubicArray/setRepeatNumberY       20\n/gate/block/cubicArray/setRepeatNumberZ       20\n/gate/block/cubicArray/setRepeatVector        0.0 1.6 2.0 cm\n\n\n#	R E P E A T HEAD\n/gate/head/repeaters/insert                   ring\n/gate/head/ring/setRepeatNumber               4\n\n\n#	A T T A C H    S Y S T E M \n/gate/systems/cylindricalPET/rsector/attach   head\n/gate/systems/cylindricalPET/module/attach    block\n/gate/systems/cylindricalPET/crystal/attach   crystal\n/gate/systems/cylindricalPET/layer0/attach    LSO\n/gate/systems/cylindricalPET/layer1/attach    BGO\n\n#	A T T A C H    C R Y S T A L  SD\n\n/gate/LSO/attachCrystalSD\n/gate/BGO/attachCrystalSD\n')
