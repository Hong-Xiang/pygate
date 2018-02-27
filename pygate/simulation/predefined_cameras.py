from pygate.components.geometry import *


def cylindricalPET(world: Volume, cylinder=None, rrh=None,
                              head=None, rcb=None, block=None, rcc=None,
                              crystal=None, lso=None, bgo=None):
    if cylinder is None:
        cylinder = Cylinder('cylindricalPET', rmax=52.0, rmin=39.9, height=40.2, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
    if rrh is None:
        rrh = RepeaterRing(number=4)
    if head is None:
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44, 0, 0, 'cm'), repeaters=[rrh])
    if rcb is None:
        rcb = RepeaterCubic(scale=Vec3(1, 5, 5, ''),
                            repeat_vector=Vec3(0.0, 3.2, 4.0))
    if block is None:
        block = Box('block', Vec3(30, 16, 20, 'mm'),
                    'Air', head, repeaters=[rcb])
    if rcc is None:
        rcc = RepeaterCubic(scale=Vec3(1, 20, 20, ''),
                            repeat_vector=Vec3(0.0, 1.6, 2.0, unit='cm'))
    if crystal is None:
        crystal = Box('crystal', Vec3(30, 3, 3.8, 'mm'),
                      'Air', block, repeaters=[rcc])
    if lso is None:
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
    if bgo is None:
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))

    sys = CylindricalPET(
        head, block, crystal=crystal, layer0=lso, layer1=bgo)
    sen_list = [crystal, ]
    cam = Camera(sys, sen_list)
    return cam


def ecat(world: Volume, cylinder=None, rlb=None, rrb=None,
                    block=None, rcc=None, crystal=None):
    if cylinder is None:
        cylinder = Cylinder('ecat', rmax=44.2, rmin=41.2, height=15.52, material='Air',
                            mother=world, unit='cm')
    if rlb is None:
        rlb = RepeaterLinear(number=4, repeat_vector=Vec3(0, 0, 38.8))
    if rrb is None:
        rrb = RepeaterRing(number=72)
    if block is None:
        block = Box('block', size=Vec3(30, 35.8594, 38.7), position=Vec3(427.0, 0.0, 0.0),
                    material='Air', mother=cylinder, repeaters=[rlb, rrb])
    if rcc is None:
        rcc = RepeaterCubic(scale=Vec3(1, 8, 8, ''),
                            repeat_vector=Vec3(0, 4.4942, 4.85))
    if crystal is None:
        crystal = Box('crystal', size=Vec3(30.0, 4.4, 4.75),
                      material='BGO', mother=block, repeaters=[rcc])

    sys = Ecat(block, crystal)
    sen_list = [crystal, ]
    cam = Camera(sys, sen_list)
    return cam


def opticalsystem(world: Volume, box = None, crystal = None,
                             rcp = None, pixel = None):
    if box is None:
        box = Box('OpticalSystem', size=Vec3(
            5.0, 5.0, 5.0, 'cm'), material='Air', mother=world)
    if crystal is None:
        crystal = Box('crystal', Vec3(30, 30, 10), position=Vec3(
            0.0, 0.0, 5.0), material='LYSO', mother=box)
    if rcp is None:
        rcp = RepeaterCubic(Vec3(10, 10, 10), repeat_vector=Vec3(3.0, 3.0, 0.0))
    if pixel is None:
        pixel = Box('pixel', Vec3(3.0, 3.0, 1.0), position=Vec3(
            0, 0, -0.5), material='G4_SILICON_DIOXIDE', mother=crystal, repeaters=[rcp])
    sys = OpticalSystem(crystal, pixel)
    sen_list = []
    cam = Camera(sys, sen_list)
    return cam


def multipatchPET(world: Volume):
    world = Box('world', Vec3(50, 50, 50, 'cm'))

    box = Box('multiPatchPET', size=Vec3(
        40.0, 40.0, 40.0, 'cm'), material='Air', mother=world)
    container = Sphere('container', rmax=17, rmin=15, phi_start=0, delta_phi=360, theta_start=0, delta_theta=180,
                       material='Air', mother=box)
    patch_list = Patch('patch', patch_file='patch1.pat',
                       material='LYSO', mother=container)
    # to be completed
    sys = MultiPatchPET(container, patch_list)
    sen_list = [patch_list]
    cam = Camera(sys, sen_list)
    return cam

def optical_surfaces():
    pass



# class Camera:
#     def __init__(self, name, world=None, detector=None):
#         self.name = name
#         self.world = None
#         self.detector = detector
#         self.geo_list = []
#         self.crystalSD_list = []
#         self.attach_list = []

#     def add_geo(self, item):
#         self.geo_list.append(item)

#     def add_crystalSD(self, item):
#         self.crystalSD_list.append(item)

#     # called after the geometry is defined in deritives.
#     def set_world(self, world):
#         if world is None:
#             maxsize = self.detector.getDiameter()
#             # set the world size to 5 time of the diamter of the detector if it is not given.
#             worldsize = geometry.Vec3(5*maxsize, 5*maxsize, 5*maxsize)
#             self.world = geometry.Box(name='world', size=worldsize)
#         else:
#             self.world = world

#     def composite(self):
#         self.world.add_child(self.detector)
