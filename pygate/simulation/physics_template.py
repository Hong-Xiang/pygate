from ..components.physics import *

# used in cylindricalPET ,ecat and multiPatchPET systems.


def pet_physics():
    return Physics([PhotoElectric, Compton, ElectronIonisation,
                    Bremsstrahlung, PositronAnnihilation, MultipleScattering], cut_pair_list)


class PET(Physics):
    def __init__(self, cut_pair_list=None):
        super().__init__([PhotoElectric, Compton, ElectronIonisation,
                          Bremsstrahlung, PositronAnnihilation, MultipleScattering], cut_pair_list)

# used in SPECThead system


class SPECT(Physics):
    def __init__(self, cut_pair_list=None):
        super().__init__([PhotoElectric, Compton, RayleighScattering,
                          ElectronIonisation, MultipleScattering], cut_pair_list)


# used in Optical simulation for visable light.
class Optical(Physics):
    def __init__(self, cut_pair_list=None):
        super().__init__(cut_pair_list)


# used in Optical simulatin for gamma.
class OpticalGamma(Physics):
    def __init__(self, cut_pair_list=None):
        super().__init__(cut_pair_list)
