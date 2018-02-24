from .base import ObjectWithTemplate
from .geometry import Volume
from typing import TypeVar as TV
from typing import List, Dict


class PhysicsProcess(ObjectWithTemplate):
    name = None
    models = ('StandardModel',)
    template = 'physics_process'

    def content_in_adding(self):
        return self.name


class PhotoElectric(PhysicsProcess):
    name = 'PhotoElectric'


class Compton(PhysicsProcess):
    name = 'Compton'


class RayleighScattering(PhysicsProcess):
    name = 'RayleighScattering'
    models = ('PenelopeModel',)


class ElectronIonisation(PhysicsProcess):
    name = 'ElectronIonisation'
    models = ('StandardModel e-', 'StandardModel e+')


class Bremsstrahlung(PhysicsProcess):
    name = 'Bremsstrahlung'
    models = ('StandardModel e-', 'StandardModel e+')


class PhysicsProcessWithoutModels(PhysicsProcess):
    models = tuple()


class PositronAnnihilation(PhysicsProcessWithoutModels):
    name = 'PositronAnnihilation'


class OpticalAbsorption(PhysicsProcessWithoutModels):
    name = 'OpticalAbsorption'


class OpticalRayleigh(PhysicsProcessWithoutModels):
    name = 'OpticalRayleigh'


class OpticalBoundary(PhysicsProcessWithoutModels):
    name = 'OpticalBoundary'


class OpticalMie(PhysicsProcessWithoutModels):
    name = 'OpticalMie'


class OpticalWLS(PhysicsProcessWithoutModels):
    name = 'OpticalWLS'


class Scintillation(PhysicsProcessWithoutModels):
    name = 'Scintillation'


class MultipleScattering(PhysicsProcess):
    name = 'MultipleScattering'

    def __init__(self, particle):
        self.p = particle

    def content_in_adding(self):
        return "{} {}".format(self.name, self.p)


class PhysicsList(ObjectWithTemplate):
    template = 'physics_list'

    def __init__(self, physics_processes: List[PhysicsProcess]):
        self.pps = physics_processes


def standard_physics_list():
    return PhysicsList((PhotoElectric(), Compton(), RayleighScattering(),
                        ElectronIonisation(), Bremsstrahlung(), PositronAnnihilation(),
                        MultipleScattering('e-'), MultipleScattering('e+')))


class Cuts(ObjectWithTemplate):
    template = 'cuts'
    STD_PARTICLES = ('Gamma', 'Electron', 'Positron')

    def __init__(self, volume: Volume, cuts: TV('CutT', float, Dict[Volume, float]), max_step: float=None):
        """
        All units are mm.
        cuts: map from partical name to cut.
        """
        self.volume = volume
        if isinstance(cuts, float):
            cuts = {k: cuts for k in self.STD_PARTICLES}
        self.cuts = cuts
        self.max_step = max_step


class Physics(ObjectWithTemplate):
    template = 'physics'

    def __init__(self, physics_list, cuts_list):
        self.pl = physics_list
        self.cl = cuts_list
