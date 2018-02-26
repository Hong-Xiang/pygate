from ..components import physics as phy
from ..components import parameter as para
from ..components import ObjectWithTemplate
from ..components import geometry as geo
from ..components.simulation import * 

from .predefined_cameras import *
from .predefined_phantoms import*
from .predefined_digitizers import *
from .predefined_physics import*
#from .predefined_parameters import*





def make_default_physics(simu_name, cut_pair_list):
    # decide the cut pair list
    if simu_name is 'PETscanner' or 'cylindricalPET' or 'ecat' or 'multiPatchPET':
         return phy.PET(cut_pair_list)
    elif simu_name is 'SPECThead':
         physics = phy.SPECT(cut_pair_list)
    elif f.camera.name is 'OpticalSystem':
         .physics = phy.OpticalPhysics(cut_pair_list)
    elif f.camera.name is 'OpticalGamma':
         .physics = phy.OpticalGamma(cut_pair_list)
    else:
        raise ValueError(
            "simulation<set_physics> invalid system name: {}".format(self.camera.name))

def make_default_parameter():
    if self.camera.name is 'OpticalSystem' or 'OpticalGamma':
        self.parameter = para.Parameter(acquisition=para.AcquisitionPrimaries(), output=para.Ascii(file_name=self.camera.name),
                                        random_engine=para.RandomEngine())
    elif self.camera.name is 'PETscanner'
        pass
    else:
        pass
def make_default_digitizer(self):
    pass



def simu():
    

if __name__ == '__main__':
    
    ## must be given parts
    #####################
    #####################
    
    # define the world volume
    world = geo.Box(name='world',size = geo.Vec3(400,400,400,'cm'))
    # define the camera
    cam = Predefined_CylindricalPET(world)
    # define the phantom
    phan =  Predefined_Voxelized_Phantom(world)
    # define the source
    source = 

    #####################
    #####################

    ##optional parts
    #####################
    #####################
    
    #phy = pet_physics()
    digi = ecat_digitizer(cam)
    




    simu = Simulation(world,cam,phan,source)
    
            if physics is None:
                self.set_physics_default()
        if parameter is None:
            self.set_parameter_default()
        if digitizer is None:
            self.set_digitizer_default()




