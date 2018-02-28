from ..components import ObjectWithTemplate
from .geometry import Geometry
from .misc import MaterialDatabaseLocal, Visualisation


class Simulation(ObjectWithTemplate):
    template = 'simulation'
    system_list = ["PETscanner","ecat","cylindricalPET","multiPatchPET","SPECThead","OpticalSystem"]
    def __init__(self,
                 geometry,
                 digitizer,
                 source,
                 parameter,
                 physics,
                 material_database=None,
                 visualisation=None):
        self.geometry = geometry
        self.digitizer = digitizer
        self.source = source
        self.parameter = parameter
        self.physics = physics
        self.material_database = material_database or MaterialDatabaseLocal()
        self.visualisation = visualisation or Visualisation()
