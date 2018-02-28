from ..components.physics import *

# used in cylindricalPET ,ecat and multiPatchPET systems.


def pet_physics(cut_pair_list):
    return Physics([PhotoElectric(), Compton(), ElectronIonisation(),
                    RayleighScattering( models = (LivermoreModel(),)),
                    Bremsstrahlung(), PositronAnnihilation(),
                    RadioactiveDecay(), MultipleScattering('e+'), MultipleScattering('e-')], cut_pair_list)


def optical_physics(cut_pair_list):
    return Physics([OpticalAbsorption(), OpticalRayleigh(), OpticalBoundary(),
                    OpticalMie(), OpticalWLS(), Scintillation(),
                    PhotoElectric(), Compton(), RayleighScattering(),
                    ElectronIonisation(), Bremsstrahlung(),
                    EMultipleScattering('e+'), EMultipleScattering('e-')], cut_pair_list)


def gamma_physics(cut_pair_list):
    return Physics([PhotoElectric(), Compton(), RayleighScattering(),
                    ElectronIonisation(), Bremsstrahlung(),
                    EMultipleScattering('e+'), EMultipleScattering('e-')], cut_pair_list)


def spect_physics(cut_pair_list):
    return Physics([], cut_pair_list)
