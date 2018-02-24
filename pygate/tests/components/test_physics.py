import unittest
from pygate.components.physics import *
from pygate.components.geometry import *


class TestStandardPhysicsList(unittest.TestCase):
    def test_render(self):
        std_pl = standard_physics_list()
        self.assertEqual(std_pl.render(),
                         '/gate/physics/addProcess PhotoElectric\n/gate/physics/processes/PhotoElectric/setModel StandardModel\n \n/gate/physics/addProcess Compton\n/gate/physics/processes/Compton/setModel StandardModel\n \n/gate/physics/addProcess RayleighScattering\n/gate/physics/processes/RayleighScattering/setModel PenelopeModel\n \n/gate/physics/addProcess ElectronIonisation\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e-\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e+\n \n/gate/physics/addProcess Bremsstrahlung\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e-\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e+\n \n/gate/physics/addProcess PositronAnnihilation\n \n/gate/physics/addProcess MultipleScattering e-\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n \n/gate/physics/addProcess MultipleScattering e+\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n \n/gate/physics/processList Enabled\n/gate/physics/processList Initialized\n')


class TestCuts(unittest.TestCase):
    def test_render(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44, 0, 0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head)
        crystal = Box('crystal', Vec3(30, 3, 3.8, 'mm'), 'Air', block)
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        phantom = Box('phantom', Vec3(10, 10, 10, 'cm'), 'Water', world)
        c = Cuts(lso, 10.0)
        self.assertEqual(c.render(),
                         '/gate/physics/Gamma/SetCutInRegion      LSO 10.0 mm\n/gate/physics/Electron/SetCutInRegion      LSO 10.0 mm\n/gate/physics/Positron/SetCutInRegion      LSO 10.0 mm\n')

    def test_render_with_max_step(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44, 0, 0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head)
        crystal = Box('crystal', Vec3(30, 3, 3.8, 'mm'), 'Air', block)
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        phantom = Box('phantom', Vec3(10, 10, 10, 'cm'), 'Water', world)
        c = Cuts(phantom, 0.1, 0.01)
        self.assertEqual(c.render(),
                         '/gate/physics/Gamma/SetCutInRegion      phantom 0.1 mm\n/gate/physics/Electron/SetCutInRegion      phantom 0.1 mm\n/gate/physics/Positron/SetCutInRegion      phantom 0.1 mm\n/gate/physics/SetMaxStepSizeInRegion    phantom 0.01 mm\n')


class TestPhysics(unittest.TestCase):
    def test_render(self):
        world = Box('world', Vec3(400.0, 400.0, 400.0, 'cm'))
        cylinder = Cylinder('cylindricalPET', 52.0, 39.9, 40.2, material='Air',
                            mother=world, position=Vec3(0.0, 0.0, 0.0, 'cm'), unit='cm')
        head = Box('head', Vec3(8, 32, 40, 'cm'), 'Air',
                   cylinder, Vec3(44, 0, 0, 'cm'))
        block = Box('block', Vec3(30, 16, 20, 'mm'), 'Air', head)
        crystal = Box('crystal', Vec3(30, 3, 3.8, 'mm'), 'Air', block)
        lso = Box('LSO', Vec3(15, 3.0, 3.8), 'LSO',
                  crystal, Vec3(-0.75, 0.0, 0.0, 'cm'))
        bgo = Box('BGO', Vec3(15, 3.0, 3.8), 'BGO',
                  crystal, Vec3(0.75, 0.0, 0.0, 'cm'))
        phantom = Box('phantom', Vec3(10, 10, 10, 'cm'), 'Water', world)
        std_pl = standard_physics_list()
        cuts_list = [Cuts(lso, 10.0), Cuts(bgo, 10.0),
                     Cuts(phantom, 0.1, 0.01)]
        phys = Physics(std_pl, cuts_list)
        self.assertEqual(phys.render(),
                         '/gate/physics/addProcess PhotoElectric\n/gate/physics/processes/PhotoElectric/setModel StandardModel\n \n/gate/physics/addProcess Compton\n/gate/physics/processes/Compton/setModel StandardModel\n \n/gate/physics/addProcess RayleighScattering\n/gate/physics/processes/RayleighScattering/setModel PenelopeModel\n \n/gate/physics/addProcess ElectronIonisation\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e-\n/gate/physics/processes/ElectronIonisation/setModel StandardModel e+\n \n/gate/physics/addProcess Bremsstrahlung\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e-\n/gate/physics/processes/Bremsstrahlung/setModel StandardModel e+\n \n/gate/physics/addProcess PositronAnnihilation\n \n/gate/physics/addProcess MultipleScattering e-\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n \n/gate/physics/addProcess MultipleScattering e+\n/gate/physics/processes/MultipleScattering/setModel StandardModel\n \n/gate/physics/processList Enabled\n/gate/physics/processList Initialized\n\n/gate/physics/Gamma/SetCutInRegion      LSO 10.0 mm\n/gate/physics/Electron/SetCutInRegion      LSO 10.0 mm\n/gate/physics/Positron/SetCutInRegion      LSO 10.0 mm\n\n/gate/physics/Gamma/SetCutInRegion      BGO 10.0 mm\n/gate/physics/Electron/SetCutInRegion      BGO 10.0 mm\n/gate/physics/Positron/SetCutInRegion      BGO 10.0 mm\n\n/gate/physics/Gamma/SetCutInRegion      phantom 0.1 mm\n/gate/physics/Electron/SetCutInRegion      phantom 0.1 mm\n/gate/physics/Positron/SetCutInRegion      phantom 0.1 mm\n/gate/physics/SetMaxStepSizeInRegion    phantom 0.01 mm\n\n')
