from ..components.simulation import *
from ..components.geometry.volume import *
from .predefined_cameras import *
from .predefined_phantoms import *
from .predefined_physics import *
from .predefined_digitizers import *
from .predefined_sources import * 
from .predefined_parameters import *

# for reference
simu_list = ['PETscanner','cylindricalPET','ecat','multiPatchPET','SPECThead','OpticalSystem','OpticalGamma']

def make_default_camera(simu_name, world:Volume):
    if simu_name is 'cylindricalPET':
        return cylindricalPET(world)
    elif simu_name is 'ecat':
        return ecat(world)
    elif simu_name in ['OpticalSystem', 'OpticalGamma']:
        return opticalsystem(world)
    elif simu_name is 'multiPatchPET':
        return multipatchPET(world)
    else:
        raise ValueError()

def make_default_surfaces(simu_name):
    pass

def make_default_physics(simu_name,  cut_pair_list = None):
    # decide the cut pair list
    if cut_pair_list is None:
        pass

    if simu_name in ['PETscanner','cylindricalPET','ecat', 'multiPatchPET']:
         return pet_physics(cut_pair_list)
    elif simu_name is 'SPECThead':
         return spect_physics(cut_pair_list)
    elif simu_name is 'OpticalSystem':
         return optical_physics(cut_pair_list)
    elif simu_name is 'OpticalGamma':
         return gamma_physics(cut_pair_list)
    else:
        raise ValueError(
            "simulation<set_physics> invalid system name: {}".format(simu_name))


def make_default_digitizer(simu_name, cam:Camera):
    if simu_name is 'cylindricalPET':
        return cylindricalPET_digitizer()
    elif simu_name is 'ecat':
        return ecat_digitizer(dtvolume = cam.system.attach_systems.block)
    elif simu_name is 'OpticalSystem':
        return optical_digitizer()
    pass

def make_default_parameter(simu_name):
    if simu_name is 'OpticalSystem' or 'OpticalGamma':
        return  optical_parameters()
    elif simu_name is 'PETscanner':
        pass
    else:
        pass
    