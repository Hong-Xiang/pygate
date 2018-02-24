import yaml


class CutPair:
    def __init__(self, region=None, cutValue=None):
        self.cutValue = cutValue
        self.region = region


class MaxStep:
    def __init__(self, region=None, maxstepsize=None):
        self.maxstepsize = maxstepsize
        self.region = region


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


class PositronAnnihilation(PhysicsProcess):
    name = 'PositronAnnihilation'
    models = tuple()


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


STD_PHYSICS_LIST = PhysicsList((PhotoElectric(), Compton(), RayleighScattering(),
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

        if isinstance(cuts, float):
            cuts = {k: cuts for k in self.STD_PARTICLES}
        self.cuts = cuts
        self.max_step = max_step


class Physics(ObjectWithTemplate):
    template = 'physics'

    def __init__(self, pyhsics_list, cuts_list):
        self.pl = pyhsics_list
        self.cl = cuts_list

    def getModelStr(self):
        return(r"/gate/physics/addProcess PhotoElectric" + "\n"
               + "/gate/physics/processes/PhotoElectric/setModel StandardModel" + "\n"
               + r"/gate/physics/addProcess Compton" + "\n"
               + r"/gate/physics/processes/Compton/setModel StandardModel" + "\n"
               + r"/gate/physics/addProcess RayleighScattering" + "\n"
               + r"/gate/physics/processes/RayleighScattering/setModel PenelopeModel" + "\n"
               + r"/gate/physics/addProcess ElectronIonisation" + "\n"
               + r"/gate/physics/processes/ElectronIonisation/setModel StandardModel e-" + "\n"
               + r"/gate/physics/processes/ElectronIonisation/setModel StandardModel e+" + "\n"
               + r"/gate/physics/addProcess Bremsstrahlung" + "\n"
               + r"/gate/physics/processes/Bremsstrahlung/setModel StandardModel e-" + "\n"
               + r"/gate/physics/processes/Bremsstrahlung/setModel StandardModel e+" + "\n"
               + r"/gate/physics/addProcess PositronAnnihilation" + "\n"
               + r"/gate/physics/addProcess MultipleScattering e+" + "\n"
               + r"/gate/physics/addProcess MultipleScattering e-" + "\n"
               # +r"/gate/physics/addProcess eMultipleScattering" + "\n"
               # +r"/gate/physics/processes/eMultipleScattering/setGeometricalStepLimiterType e- distanceToBoundary" + "\n"
               # +r"/gate/physics/processes/eMultipleScattering/setGeometricalStepLimiterType e+ distanceToBoundary" + "\n"
               # +r"/gate/physics/addProcess RadioactiveDecay" + "\n"
               # +r"/gate/physics/addAtomDeexcitation" + "\n"
               + r"/gate/physics/processList Enabled" + "\n"
               + r"/gate/physics/processList Initialized" + "\n")

    def addCutPair(self, item):
        if item.cutValue is None or item.region is None:
            pass
        else:
            self.cutPairList.append(item)

    def addMaxStep(self, item):
        if item.maxstepsize is None or item.region is None:
            pass
        else:
            self.maxstepsizeList.append(item)

    def getMacStr(self):
        fmt1 = r"/gate/physics/Gamma/SetCutInRegion {0}  {1}" + " mm\n"
        fmt2 = r"/gate/physics/Electron/SetCutInRegion {0}  {1}" + " mm\n"
        fmt3 = r"/gate/physics/Positron/SetCutInRegion {0}  {1}" + " mm\n"

        fmt4 = r"/gate/physics/SetMaxStepSizeInRegion {0} {1}" + " mm\n"
        Str = ""
        for item in self.cutPairList:
            Str += fmt1.format(item.region, item.cutValue)
            Str += fmt2.format(item.region, item.cutValue)
            Str += fmt3.format(item.region, item.cutValue)
        for item in self.maxstepsizeList:
            Str += fmt4.format(item.region, item.maxstepsize)
        return (self.getModelStr() + Str)

# if __name__ == '__main__':
#     phy = Physics()
#     phy.addCutPair(CutPair(region = 'level1', cutValue = 10 ))
#     print(phy.getMacStr())
#     with open('physics.yml', 'w') as fout:
#         yaml.dump(phy, fout)
