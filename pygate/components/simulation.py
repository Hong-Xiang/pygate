from ..components import ObjectWithTemplate
from .geometry import Volume
from .misc import MaterialDatabaseLocal


class Simulation(ObjectWithTemplate):
    template = 'simulation'

    def __init__(self,
                 world: Volume,
                 surfaces,
                 camera,
                 phantom,
                 digitizer,
                 source,
                 parameter,
                 physics,
                 material_database=None,
                 visualisation=None):
        self.world = world
        self.camera = camera
        self.phantom = phantom
        self.digitizer = digitizer
        self.source = source
        self.parameter = parameter
        self.physics = physics
        self.material_database = material_database or MaterialDatabaseLocal()
        self.visualisation = visualisation
