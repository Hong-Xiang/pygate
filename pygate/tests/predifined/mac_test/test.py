from pygate.components.geometry.volume import *
from pygate.predefined.simulations import *

# from pygate.components.physics import EMultipleScattering
# if __name__ =='__main__':
    
    # print(EMultipleScattering('e+').render())

if __name__ == '__main__':
 
    #####################
    #####################
    simu_name = 'OpticalSystem'
    simu = make_simulation(simu_name)
    with open('./pygate/mac_test/OpticalSystem.txt', 'w') as fout:
        print(simu.render(), file=fout)
    print("OK!\n")