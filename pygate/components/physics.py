from .base import ObjectWithTemplate
from .geometry import Volume
from typing import TypeVar as TV
from typing import List, Dict


class Model(ObjectWithTemplate):
    name = None
    template = 'physics/model'

    def __init__(self, particle=None):
        self.particle = particle
        self.process = None


class PenelopeModel(Model):
    name = 'PenelopeModel'


class StandardModel(Model):
    name = 'StandardModel'

class LivermoreModel(Model):
    name = 'LivermoreModel'

class LivermorePolarizedModel(Model):
    name = 'LivermorePolarizedModel'




class PhysicsProcess(ObjectWithTemplate):
    name = None
    template = 'physics/process'

    def __init__(self, models=None):
        if models is None:
            models = (StandardModel(),)
        self.models = models
        for m in self.models:
            m.process = self

    def content_in_adding(self):
        return self.name


class PhotoElectric(PhysicsProcess):
    name = 'PhotoElectric'


class Compton(PhysicsProcess):
    name = 'Compton'

class GammaConversion(PhysicsProcess):
    name = 'GammaConversion'

class RayleighScattering(PhysicsProcess):
    name = 'RayleighScattering'

    def __init__(self, models=(PenelopeModel(),)):
        super().__init__(models)


class ElectronIonisation(PhysicsProcess):
    name = 'ElectronIonisation'

    def __init__(self, models=(StandardModel('e-'),
                               StandardModel('e+'))):
        super().__init__(models)


class Bremsstrahlung(PhysicsProcess):
    name = 'Bremsstrahlung'

    def __init__(self, models=(StandardModel('e-'),
                               StandardModel('e+'))):
        super().__init__(models)


class PhysicsProcessWithoutModels(PhysicsProcess):
    def __init__(self):
        super().__init__(tuple())



class PositronAnnihilation(PhysicsProcessWithoutModels):
    name = 'PositronAnnihilation'

class RadioactiveDecay(PhysicsProcessWithoutModels):
    name = 'RadioactiveDecay'

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


class MultipleScattering(PhysicsProcessWithoutModels):
    name = 'MultipleScattering'

    def __init__(self, particle):
        super().__init__()
        self.p = particle

    def content_in_adding(self):
        return "{} {}".format(self.name, self.p)

class EMultipleScattering(PhysicsProcessWithoutModels):
    name = 'eMultipleScattering'
    
    def __init__(self, particle):
        super().__init__()
        self.p = particle

    def content_in_adding(self):
        return "{} {}".format(self.name, self.p)

class PhysicsList(ObjectWithTemplate):
    template = 'physics/list'

    def __init__(self, physics_processes: List[PhysicsProcess]):
        self.pps = physics_processes


class Cuts(ObjectWithTemplate):
    template = 'physics/cuts'
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
    template = 'physics/physics'

    def __init__(self, physics_list, cuts_list):
        self.pl = physics_list
        self.cl = cuts_list
