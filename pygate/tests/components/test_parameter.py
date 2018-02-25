import unittest
from pygate.utils.strs import assert_equal_ignoring_multiple_whitespaces as ae
from pygate.components.parameter import *


class TestRandomEngine(unittest.TestCase):
    def test_render(self):
        re = RandomEngine()
        ae(self, re.render(),
           '/gate/random/setEngineName JamesRandom\n/gate/random/setEngineSeed default\n')


class TestRandomEngineJamesRandom(unittest.TestCase):
    def test_render(self):
        re = RandomEngineJamesRandom()
        ae(self, re.render(),
           '/gate/random/setEngineName JamesRandom\n/gate/random/setEngineSeed default\n')


class TestRoot(unittest.TestCase):
    def test_render(self):
        root = Root('result', 0, 1, 1)
        ae(self, root.render(),
           '/gate/output/root/enable\n/gate/output/root/setFileName  result\n/gate/output/root/setRootHitFlag    0\n/gate/output/root/setRootSinglesFlag    1\n/gate/output/root/setRootCoincidencesFlag    1\n')


class TestSinogram(unittest.TestCase):
    def test_render(self):
        class DummyInput:
            name = 'finalcoin'
        sino = Sinogram('sinogram', DummyInput(), None,
                        None, True, 1.8, 1.8, True, True)
        ae(self, sino.render(),
           '/gate/output/sinogram/enable\n/gate/output/sinogram/setFileName  sinogram\n/gate/output/sinogram/setTangCrystalBlurring 1.8 mm\n/gate/output/sinogram/setAxialCrystalBlurring 1.8 mm\n/gate/output/sinogram/RawOutputEnable true\n/gate/output/sinogram/StoreDelayeds\n/gate/output/sinogram/StoreScatters\n/gate/output/sinogram/setInputDataName finalcoin\n')


class TestAcquisitionPeriod(unittest.TestCase):
    def test_render(self):
        ap = AcquisitionPeriod(0.0, 0.1, 0.1)
        ae(self, ap.render(),
           '/gate/application/setTimeStart  0 s\n/gate/application/setTimeStop  0.1 s\n        /gate/application/setTimeSlice  0.1 s\n/gate/application/startDAQ\n')
