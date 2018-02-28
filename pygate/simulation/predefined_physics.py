from ..components.physics import *
from ..
# used in cylindricalPET ,ecat and multiPatchPET systems.


def pet_physics(cam, phantom):
    cut_pair_list = []
    return Physics([PhotoElectric, Compton, ElectronIonisation,
                    Bremsstrahlung, PositronAnnihilation, MultipleScattering], cut_pair_list)
def spect_physics():
    pass