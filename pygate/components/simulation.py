from ..components import ObjectWithTemplate
from .geometry import Geometry
from .misc import MaterialDatabaseLocal, Visualisation


class Simulation(ObjectWithTemplate):
    template = 'simulation'
    def __init__(self,
                 geometry,
                 physics,
                 digitizer,
                 source,
                 parameter,
                 material_database=None,
                 visualisation=None):
        self.geometry = geometry
        self.digitizer = digitizer
        self.physics = physics
        self.source = source
        self.parameter = parameter
        self.material_database = material_database or MaterialDatabaseLocal()
        self.visualisation = visualisation or Visualisation()
