import physics_template as phy
from ..components import parameter as para
from ..components import ObjectWithTemplate
from .camera import Camera


class Simulation(ObjectWithTemplate):
    template = 'simulation'
    system_list = ["PETscanner","ecat","cylindricalPET","multiPatchPET","SPECThead","OpticalSystem"]
    def __init__(self,
                 world:Volume,
                 camera:Camera,
                 phantom:Phantom,
                 source:SourceList,
                 physics=None,
                 parameter=None,
                 digitizer=None, visualisation=None):
        self.world = world
        self.camera = camera
        self.phantom = phantom
        self.source = source
        
        self.digitizer = digitizer
        self.physics = physics
        self.parameter = parameter


# if __name__ == '__main__':
#     simu1 = SimuApp(camera.name='ecat')
