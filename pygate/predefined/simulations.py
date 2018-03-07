from enum import Enum
from ..components.simulation import *
from ..components.geometry.volume import *
from ..components.geometry.camera import Camera
from ..components.geometry.phantom import Phantom
from ..components.geometry.surface import *
from ..components.physics import Cuts
from .cameras import *
from .phantoms import *
from .physics import *
from .digitizers import *
from .sources import *
from .parameters import *

# for reference
# simu_list = ['PETscanner','cylindricalPET','ecat','multiPatchPET','SPECThead','OpticalSystem','OpticalGamma']


class PredefinedSimulations(Enum):
    PETScanner = 'PETscanner'
    CylindricalPET = 'cylindricalPET'
    ECAT = 'ecat'
    MultiPatchPET = 'multiPatchPET'
    SPECTHead = 'SPECThead'
    OpticalSystem = 'OpticalSystem'
    OpticalGamma = 'OpticalGamma'


def make_default_camera(simu_name, world: Volume):
    if simu_name is 'cylindricalPET':
        return cylindricalPET(world)
    elif simu_name is 'ecat':
        return ecat(world)
    elif simu_name in ['OpticalSystem', 'OpticalGamma']:
        return opticalsystem(world)
    elif simu_name is 'multiPatchPET':
        return multipatchPET(world)
    else:
        raise ValueError("invalid simulation type: {}".format(simu_name))


def make_default_surfaces(simu_name, cam: Camera):
    surfaces = []
    if simu_name in ['OpticalSystem', 'OpticalGamma']:
        surfaces = optical_surfaces(cam)
    else:
        surfaces = ()
    return surfaces


def make_default_physics(simu_name, cam: Camera, phan: Phantom, cut_pair_list=None):
    # decide the cut pair list
    if cut_pair_list is None:
        cut_pair_list = []
        for v in cam.sds:
            cut_pair_list.append(Cuts(v, 0.1))
        if phan:
            for v in phan.sds:
                cut_pair_list.append(Cuts(v, 0.1))
        cut_pair_list = tuple(cut_pair_list)
    if simu_name in ['PETscanner', 'cylindricalPET', 'ecat', 'multiPatchPET']:
        return pet_physics(cut_pair_list)
    elif simu_name is 'SPECThead':
        return spect_physics(cut_pair_list)
    elif simu_name is 'OpticalSystem':
        return optical_physics(cut_pair_list=())
    elif simu_name is 'OpticalGamma':
        return gamma_physics(cut_pair_list=())
    else:
        raise ValueError(
            "simulation<set_physics> invalid system name: {}".format(simu_name))


def make_default_digitizer(simu_name, cam: Camera):
    if simu_name is 'cylindricalPET':
        return cylindricalPET_digitizer()
    elif simu_name is 'ecat':
        return ecat_digitizer(dtvolume=cam.system.levels['block'])
    elif simu_name in ['OpticalSystem', 'OpticalGamma']:
        return optical_digitizer()
    pass


def make_default_parameter(simu_name):
    if simu_name is 'OpticalSystem' or 'OpticalGamma':
        return optical_parameters()
    elif simu_name in ['PETscanner', 'ecat', 'cylindricalPET', 'multiPatchPET']:
        return pet_parameters()
    else:
        pass


def make_simulation(simu_name, geo=None, phy=None, digi=None, src=None, para=None):
       # for reference
    # simu_list = ['PETscanner','cylindricalPET','ecat','multiPatchPET','SPECThead','OpticalSystem','OpticalGamma']
    # simu_name = 'OpticalGamma'

   # must be given parts
    #####################
    #####################

    if geo is None:
        world = Box(name='world', size=Vec3(400, 400, 400, 'cm'))
        cam = make_default_camera(simu_name, world)
        surf = make_default_surfaces(simu_name, cam)
        phan = None
        # build up the geometry
        geo = Geometry(world, cam, phan, surf)

    # optional parts
    #####################
    #####################
    if phy is None:
        phy = make_default_physics(simu_name, cam, phan)
    if digi is None:
        digi = make_default_digitizer(simu_name, cam)

    # define the source
    if src is None:
        src = make_default_source(simu_name)

    # define the parameters
    if para is None:
        para = make_default_parameter(simu_name)

    # create a simulation
    simu = Simulation(geo, phy, digi, src, para)

    return simu


def simulation(simulation_name: PredefinedSimulations, geometry=None, physics=None, digitizer=None, source=None, parameter=None):
    return make_simulation(simulation_name.value, geometry, physics, digitizer, source, parameter)


def optical_gamma(source=None,
                  world_size: Vec3=Vec3(400.0, 400.0, 400.0, 'cm'),
                  crystal_size: Vec3=Vec3(30.0, 30.0, 30.0, 'mm'),
                  crystal_position: Vec3=Vec3(0.0, 0.0, 0.0, 'mm'),
                  crystal_material: str='LYSO',
                  nb_primaries=10000):
    from ..components.geometry import Box, Geometry
    from . import cameras, digitizers, physics, parameters
    world = Box('world', world_size)

    def crystal(mother): return Box('crystal', crystal_size,
                                    crystal_material, mother,
                                    crystal_position)
    return Simulation(Geometry(world, cameras.optical_gamma(world, crystal), None, ()),
                      physics.gamma_physics(()),
                      digitizers.optical_digitizer(),
                      source,
                      parameters.optical_gamma(nb_primaries))
