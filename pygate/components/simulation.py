import camera
import physics_template as phy
from ..components import parameter as para

from ..components import ObjectWithTemplate
from .camera import Camera


class Simulation(ObjectWithTemplate):
    template = 'simulation'
    system_list = ["PETscanner","ecat","cylindricalPET","multiPatchPET","SPECThead","OpticalSystem"]
    def __init__(self,
                 camera,phantom,source,
                 physics=None,
                 parameter=None,
                 digitizer=None, visualisation=None):
        self.camera = camera
        self.phantom = phantom
        self.source = source
        
        self.digitizer = digitizer
        self.physics = physics
        self.parameter = parameter

        if physics is None:
            self.set_physics_default()
        if parameter is None:
            self.set_parameter_default()
        if digitizer is None:
            self.set_digitizer_default()



    def set_physics_default(self):
        
        # decide the cut pair list

        if self.camera.name is 'PETscanner' or 'cylindricalPET' or 'ecat' or 'multiPatchPET':
            self.physics = phy.PET()
        elif self.camera.name is 'SPECThead':
            self.physics = phy.SPECT()
        elif self.camera.name is 'OpticalSystem':
            self.physics = phy.OpticalPhysics()
        elif self.camera.name is 'OpticalGamma':
            self.physics = phy.OpticalGamma()
        else:
            raise ValueError(
                "simulation<set_physics> invalid system name: {}".format(self.camera.name))

    def set_parameter_default(self):
        if self.camera.name is 'OpticalSystem' or 'OpticalGamma':
            self.parameter = para.Parameter(acquisition=para.AcquisitionPrimaries(), output=para.Ascii(file_name=self.camera.name),
                                            random_engine=para.RandomEngine())
        elif self.camera.name is 

    def set_digitizer_default(self):
        pass


# if __name__ == '__main__':
#     simu1 = SimuApp(camera.name='ecat')
