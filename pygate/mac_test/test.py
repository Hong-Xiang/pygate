from pygate.components.geometry.volume import *
from pygate.simulation.simulation import *

# from pygate.components.physics import EMultipleScattering
# if __name__ =='__main__':
    
    # print(EMultipleScattering('e+').render())

if __name__ == '__main__':
    # for reference
    # simu_list = ['PETscanner','cylindricalPET','ecat','multiPatchPET','SPECThead','OpticalSystem','OpticalGamma']
    simu_name = 'OpticalGamma'
    ## must be given parts
    #####################
    #####################
    
    # define the world volume
    world = Box(name='world',size = Vec3(400,400,400,'cm'))
    # define the camera
    cam = make_default_camera(simu_name,world)
    # define the phantom
    #phan =  voxelized_phantom(world)
    phan = None

    #define the surface when simulating optical systems
    surf =  make_default_surfaces(simu_name,cam)
    #make_default_optical_surfaces(simu_name,cam)

    #build up the geometry
    geo  = Geometry(world,cam,phan,surf)
    
    
    ##optional parts
    #####################
    #####################
    
    phy = make_default_physics(simu_name,cam, phan)
    
    digi = make_default_digitizer(simu_name,cam)

    # define the source
    #src = voxelized_gamma(position = Vec3(-10,-10,-10,'mm'))
    src = sphere_source()
    # define the parameters
    para = make_default_parameter(simu_name)
    #####################
    #####################

    simu = Simulation(geo,phy,digi,src,para)
    with open('./pygate/mac_test/OpticalGamma.txt', 'w') as fout:
        print(simu.render(), file=fout)
    print("OK!\n")




