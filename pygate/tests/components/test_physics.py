import unittest
from pygate.components.physics import *


class TestStandardPhysicsList(unittest.TestCase):
    def test_render(self):
        std_pl = standard_physics_list()
        self.assertEqual(std_pl.render(),
                         '\n/gate/physics/addProcess PhotoElectric\n/gate/physics/processes/PhotoElectric/setModel StandardModel\n\n/gate/physics/addProcess Compton\n/gate/physics/processes/Compton/setModel StandardModel\n\n/gate/physics/addProcess RayleighScattering\n/gate/physics/processes/RayleighScattering/setModel PenelopeModel\n\n/gate/physics/addProcess ElectronIonisation\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e-\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e+\n\n/gate/physics/addProcess Bremsstrahlung\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e-\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e+\n\n/gate/physics/addProcess PositronAnnihilation\n\n/gate/physics/addProcess MultipleScattering e-\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n\n/gate/physics/addProcess MultipleScattering e+\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n\n/gate/physics/processList Enabled\n/gate/physics/processList Initialized\n')
