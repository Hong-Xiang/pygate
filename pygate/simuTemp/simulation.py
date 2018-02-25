import camera
import physics_template as phy
from ..components import parameter as para


class SimuApp:
    # camera name list
    system_name_list = ["PETscanner", "cylindricalPET", "ecat",
                        "multiPatchPET", "SPECThead", "OpticalSystem", "OpticalGamma"]

    def __init__(self, system_name, camera=None, physics=None, parameter=None,
                 phantom=None, source=None, digitizer=None):
        self.system_name = system_name
        self.camera = camera
        self.physics = physics
        self.digitizer = digitizer

        self.phantomList = phantomList
        self.sourceList = sourceList

        if camera is None:
            self.set_camera_default(system_name)
        if physics is None:
            self.set_physics_default()
        if parameter is None:
            self.set_parameter_default()
        if digitizer is None:
            self.set_digitizer_default()

    def set_camera_default(self, system_name):
        if system_name in self.system_name_list:
            if system_name is 'PETscanner':
                self.system = camera.PETscanner()
            elif system_name is 'cylindricalPET':
                self.system = camera.CylindricalPET()
            elif system_name is 'ecat':
                self.system = camera.Ecat()
            elif system_name is 'multiPatchPET':
                self.system = camera.MultiPatchPET()
            elif system_name is 'SPECThead':
                self.system = camera.SPECThead()
            else:
                self.system = camera.OpticalSystem()
        else:
            raise ValueError(
                "simulation<set_system> invalid system name: {}".format(system_name))

    def set_physics_default(self):
        if self.system_name is 'PETscanner' or 'cylindricalPET' or 'ecat' or 'multiPatchPET':
            self.physics = phy.PET()
        elif self.system_name is 'SPECThead':
            self.physics = phy.SPECT()
        elif self.system_name is 'OpticalSystem':
            self.physics = phy.OpticalPhysics()
        elif self.system_name is 'OpticalGamma':
            self.physics = phy.OpticalGamma()
        else:
            raise ValueError(
                "simulation<set_physics> invalid system name: {}".format(system_name))
    
    def set_parameter_default(self):
        if self.system_name is 'OpticalSystem' or 'OpticalGamma':
            self.parameter = para.Parameter(acquisition=para.Primaries(), output=para.Ascii(file_name=self.system_name),
                                random_engine=para.RandomEngine())   
            


    def set_digitizer_default(self):
        if self.system_name is ''




if __name__ == '__main__':
    simu1 = SimuApp(system_name='ecat')