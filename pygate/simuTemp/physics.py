from ..components import physics 
class CutPairs:
    def __init__(self,region=None, value = None):
        self.value = value
        self.region = region
class Physics:
    def __init__(self, cut_pair_list):
        self.cut_pair_list = cut_pair_list


# used in cylindricalPET ,ecat and multiPatchPET systems.
class PETPhysics(Physics):
    def __init__(self, cut_pair_list = None):
        super(PETPhysics,self).__init__(cut_pair_list)
    
    # the expand part of PETPhysics  
        # /gate/physics/addProcess PhotoElectric
        # /gate/physics/processes/PhotoElectric/setModel StandardModel

        # /gate/physics/addProcess Compton
        # /gate/physics/processes/Compton/setModel StandardModel

        # /gate/physics/addProcess RayleighScattering
        # /gate/physics/processes/RayleighScattering/setModel PenelopeModel

        # /gate/physics/addProcess ElectronIonisation
        # /gate/physics/processes/ElectronIonisation/setModel StandardModel e-
        # /gate/physics/processes/ElectronIonisation/setModel StandardModel e+

        # /gate/physics/addProcess Bremsstrahlung
        # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e-
        # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e+

        # /gate/physics/addProcess PositronAnnihilation

        # /gate/physics/addProcess MultipleScattering e+
        # /gate/physics/addProcess MultipleScattering e-

        # /gate/physics/processList Enabled
        # /gate/physics/processList Initialized
        #

# used in SPECThead system 
class SPECTPhysics(Physics):
    def __init__(self,cut_pair_list = None):
        super(SPECTPhysics,self).__init__(cut_pair_list)

        # /gate/physics/addProcess PhotoElectric
        # /gate/physics/processes/PhotoElectric/setModel StandardModel

        # /gate/physics/addProcess Compton
        # /gate/physics/processes/Compton/setModel PenelopeModel

        # /gate/physics/addProcess RayleighScattering
        # /gate/physics/processes/RayleighScattering/setModel PenelopeModel

        # /gate/physics/addProcess ElectronIonisation
        # /gate/physics/processes/ElectronIonisation/setModel StandardModel e-

        # /gate/physics/addProcess Bremsstrahlung
        # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e-

        # /gate/physics/addProcess MultipleScattering e-

        # /gate/physics/processList Enabled
        # /gate/physics/processList Initialized

# used in Optical simulation for visable light.
class OpticalPhysics(Physics):
    def __init__(self,cut_pair_list = None):
        super(OpticalPhysics,self).__init__(cut_pair_list)
    
    # /gate/physics/addProcess OpticalAbsorption
    # /gate/physics/addProcess OpticalRayleigh
    # /gate/physics/addProcess OpticalBoundary
    # /gate/physics/addProcess OpticalMie
    # /gate/physics/addProcess OpticalWLS
    # /gate/physics/addProcess Scintillation


    # /gate/physics/addProcess PhotoElectric
    # /gate/physics/processes/PhotoElectric/setModel StandardModel

    # /gate/physics/addProcess Compton
    # /gate/physics/processes/Compton/setModel StandardModel

    # /gate/physics/addProcess RayleighScattering
    # /gate/physics/processes/RayleighScattering/setModel PenelopeModel

    # /gate/physics/addProcess ElectronIonisation
    # /gate/physics/processes/ElectronIonisation/setModel StandardModel e-
    # /gate/physics/processes/ElectronIonisation/setModel StandardModel e+

    # /gate/physics/addProcess Bremsstrahlung
    # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e-
    # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e+

    # /gate/physics/addProcess eMultipleScattering e+
    # /gate/physics/addProcess eMultipleScattering e-

    # /gate/physics/processList Enabled
    # /gate/physics/processList Initialized

# used in Optical simulatin for gamma.
class OpticalGamma(Physics):
    def __init__(self, cut_pair_list = None):
        super(OpticalGamma,self).__init__(cut_pair_list)
    
    # /gate/physics/addProcess PhotoElectric
    # /gate/physics/processes/PhotoElectric/setModel StandardModel

    # /gate/physics/addProcess Compton
    # /gate/physics/processes/Compton/setModel StandardModel

    # /gate/physics/addProcess RayleighScattering
    # /gate/physics/processes/RayleighScattering/setModel PenelopeModel

    # /gate/physics/addProcess ElectronIonisation
    # /gate/physics/processes/ElectronIonisation/setModel StandardModel e-
    # /gate/physics/processes/ElectronIonisation/setModel StandardModel e+

    # /gate/physics/addProcess Bremsstrahlung
    # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e-
    # /gate/physics/processes/Bremsstrahlung/setModel StandardModel e+

    # /gate/physics/addProcess eMultipleScattering e+
    # /gate/physics/addProcess eMultipleScattering e-

    # /gate/physics/processList Enabled
    # /gate/physics/processList Initialized
