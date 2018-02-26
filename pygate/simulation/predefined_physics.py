from ..components.physics import *
from ..components.camera import*
from ..components.phantom import*

# used in cylindricalPET ,ecat and multiPatchPET systems.
def pet_physics(geo:Geometry, cut_pair_list = None):
    if cut_pair_list is None:
        #generate the  
        pass
    return Physics([PhotoElectric, Compton, ElectronIonisation,
                    Bremsstrahlung, PositronAnnihilation, MultipleScattering], cut_pair_list)



def optical_physics(geo:Geometry, cut_pair_list =None):
    pass

def gamma_physics():
    pass
def spect_physics():
    pass