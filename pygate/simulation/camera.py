from ..components import geometry


class System:
    def __init__(self, name, world=None, detector=None):
        self.name = name
        self.world = None
        self.detector = detector
        self.geo_list = []
        self.crystalSD_list = []
        self.attach_list = []

    def add_geo(self, item):
        self.geo_list.append(item)

    def add_crystalSD(self, item):
        self.crystalSD_list.append(item)

    # called after the geometry is defined in deritives.
    def set_world(self, world):
        if world is None:
            maxsize = self.detector.getDiameter()
            # set the world size to 5 time of the diamter of the detector if it is not given.
            worldsize = geometry.Vec3(5*maxsize, 5*maxsize, 5*maxsize)
            self.world = geometry.Box(name='world', size=worldsize)
        else:
            self.world = world

    def composite(self):
        self.world.add_child(self.detector)


class PETscanner(System):
    def __init__(self, world=None, detector=None, level1=None, level2=None, level3=None, level4=None, level5=None):
        super(PETscanner, self).__init__(name='PETscanner')


class Ecat(System):
    def __init__(self, world=None, detector=None, block=None, crystal=None):
        super(Ecat, self).__init__(name='ecat')
        if detector is None:
            self.detector = geometry.Cylinder(
                name='ecat', rmax=442.0, rmin=412.0, height=155.2, material='Air')
        else:
            detector.name = 'ecat'
            self.detector = detector
        if block is None:
            self.block = geometry.Box(name='block', position=geometry.Vec3(427.0, 0, 0), material='Air',
                                      size=geometry.Vec3(30.0, 35.8594, 38.7))
        else:
            self.block = block
        if crystal is None:
            self.crystal = geometry.Box(name='crystal', material='BGO',
                                        size=geometry.Vec3(30.0, 4.4, 4.75))
        self.set_world(world)

    def composite(self):
        super(Ecat, self).composite()
        self.detector.add_child(self.block)
        self.block.add_child(self.crystal)


class CylindricalPET(System):
    # the complete levels of an cylindricalPET: cylindricalPET->rsector->module->submodule->crystal->layer0-3
    def __init__(self, world=None, detector=None, rsector=None, module=None, submodule=None, crystal=None,
                 layer0=None, layer1=None, layer2=None, layer3=None):
        super(CylindricalPET, self).__init__(name='cylindricalPET')
        if detector is None:
            self.ring = geometry.Cylinder(
                name='cylindricalPET', rmax=520, rmin=399, height=40.2, material='Air')
        else:
            detector.name = 'cylindricalPET'
            self.detector = detector
        if rsector is None:
            self.rsector = geometry.Box(name='head', position=geometry.Vec3(440.0, 0.0, 0.0),
                                        size=geometry.Vec3(80, 320, 400), material='Air')
        else:
            self.module = module

        # ignore the submodule if no user definition
        self.submodule = submodule

        if crystal is None:
            self.crystal = geometry.Box(name='crystal', position=geometry.Vec3(0, 0, 0),
                                        size=geometry.Vec3(30.0, 3.0, 3.8), material='Air')
        else:
            self.crystal = crystal

        if layer0 is None:
            self.layer0 = geometry.Box(name='LSO', position=geometry.Vec3(0, 0, 0),
                                       size=geometry.Vec3(30, 3.0, 3.8), material='LSO')
        else:
            self.layer0 = layer0
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3

        self.set_world(world)
        self.composite()

    # define the parent-child relationship between the geometries.
    def composite(self):
        super(CylindricalPET, self).composite()
        self.detector.add_child(self.rsector)
        self.rsector.add_child(self.module)
        if not self.submodule:
            self.module.add_child(self.submodule)
            self.submodule.add_child(self.crystal)
        else:
            self.module.add_child(self.crystal)
        self.crystal.add_child(self.layer0)
        if not self.layer1:
            self.crystal.add_child(self.layer1)
        if not self.layer2:
            self.crystal.add_child(self.layer2)
        if not self.layer3:
            self.crystal.add_child(self.layer3)

    def attach_SD(self):

        pass


class MultiPatchPET(System):
    # the complete levels of multiPatchPET: multiPatchPET->container->patches
    def __init__(self, world=None, detector=None, container=None, patchlist=None):
        super(MultiPatchPET, self).__init__(name='multiPatchPET')
        if detector is None:
            self.detector = geometry.Box(
                name='multiPatchPET', material='Air', size=geometry.Vec3(1000.0, 1000.0, 1000.0))
        else:
            detector.name = 'multiPatchPET'
            self.detector = detector
        if container is None:
            self.container = geometry.Sphere(name='container', rmax=360.0, rmin=300.0, material='Air',
                                             phi_start=0.0, delta_phi=360, theta_start=0, delta_theta=180)
        else:
            self.container = container

        self.patchlist = []
        if patchlist is None:
            print("empty patch list!  camera<MultiPatchPET>:__init__() \n")
        else:
            for item in patchlist:
                self.patchlist.append(item)
        self.set_world(world)
        self.composite()

    def composite(self):
        super(MultiPatchPET, self).composite()
        self.detector.add_child(self.container)
        for item in self.patchlist:
            self.container.add_child(item)


class SPECThead(System):
    # the complete levels of SPECThead: SPECThead->crystal->pixel
    def __init__(self, world=None, detector=None, crystal=None, pixel=None):
        super(SPECThead, self).__init__(name='SPECThead')
        if detector is None:
            self.detector = geometry.Box(name='SPECThead', position=geometry.Vec3(200.0, 0.0, 0.0), material='Air',
                                         size=geometry.Vec3(70.0, 210.0, 300.0))
        else:
            detector.name = 'SPECThead'
            self.detector = detector
        if crystal is None:
            self.crystal = geometry.Box(
                name='crystal', material='NaI', size=geometry.Vec3(10.0, 190.0, 280.0))
        else:
            self.crystal = crystal
        # ignore the pixel level if no user definition
        self.pixel = pixel

        self.set_world(world)
        self.composite()

    def composite(self):
        super(SPECThead, self).composite()
        self.detector.add_child(self.crystal)
        if not self.pixel:
            self.crystal.add_child(self.pixel)


class OpticalSystem(System):
    def __init__(self, world=None, detector=None, crystal=None, pixel=None):
        super(OpticalSystem, self).__init__(name='OpticalSystem')
        if detector is None:
            self.detector = geometry.Box(name='OpticalSystem', position=geometry.Vec3(200.0, 0.0, 0.0), material='Air',
                                         size=geometry.Vec3(70.0, 210.0, 300.0))
        else:
            detector.name = 'OpticalSystem'
            self.detector = detector
        if crystal is None:
            self.crystal = geometry.Box(
                name='crystal', material='NaI', size=geometry.Vec3(10.0, 190.0, 280.0))
        else:
            self.crystal = crystal
        # ignore the pixel level if no user definition
        if pixel is None:
            self.pixel = geometry.Box(
                name='pixel', material='LYSO', size=geometry.Vec3(10.0, 190.0, 280.0))
        else:
            self.pixel = pixel

        self.set_world(world)
        self.composite()

    def set_geometry(self):
        return
