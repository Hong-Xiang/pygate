from pygate.components.geometry.volume import *
from pygate.simulation.simulation import *

if __name__ == '__main__':
    
    simu_name = 'cylindricalPET'
    ## must be given parts
    #####################
    #####################
    
    # define the world volume
    world = Box(name='world',size = Vec3(400,400,400,'cm'))
    # define the camera
    cam = cylindricalPET(world)
    # define the phantom
    phan =  voxelized_phantom(world)

    #define the surface when simulating optical systems
    surf =  []

    #build up the geometry
    geo  = Geometry(world,cam,phan,surf)
    
    
    ##optional parts
    #####################
    #####################
    
    phy = make_default_physics(simu_name,cam)
    
    digi = make_default_digitizer(simu_name,cam)

    # define the source
    src = voxelized_gamma(position = Vec3(-10,-10,-10))

    # define the parameters
    para = pet_parameters()
    #####################
    #####################

    simu = Simulation(geo,phy,digi,src,para)
    print(simu.render())
    print("OK!\n")




