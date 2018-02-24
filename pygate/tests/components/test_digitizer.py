import unittest
from pygate.utils.strs import ignore_empty_newlines
from pygate.components.digitizer import *


class TestAdder(unittest.TestCase):
    def test_render(self):
        adder = Adder()
        singles = Singles([adder])

        to_compare = [adder.render(),
                      '/gate/digitizer/Singles/insert adder\n']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestReadout(unittest.TestCase):
    def test_render(self):
        readout = Readout()
        singles = Singles([readout])
        to_compare = [readout.render(),
                      '/gate/digitizer/Singles/insert readout\n/gate/digitizer/Singles/readout/setPolicy TakeEnergyCentroid\n/gate/digitizer/Singles/readout/setDepth  1\n']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestBlurring(unittest.TestCase):
    def test_render(self):
        blur = Blurring(resolution=0.1, eor=511)
        singles = Singles([blur])
        to_compare = [blur.render(),
                      '/gate/digitizer/Singles/insert blurring\n/gate/digitizer/Singles/blurring/setResolution 0.1\n/gate/digitizer/Singles/blurring/setEnergyOfReference 511 keV\n']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestThresHold(unittest.TestCase):
    def test_render(self):
        thres = ThresHolder(250)
        singles = Singles([thres])
        to_compare = [thres.render(),
                      '/gate/digitizer/Singles/insert thresholder\n/gate/digitizer/Singles/thresholder/setThreshold 250 keV\n']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestUpHolder(unittest.TestCase):
    def test_render(self):
        uph = ThresHolder(750)
        singles = Singles([uph])
        to_compare = [uph.render(),
                      '/gate/digitizer/Singles/insert upholder\n/gate/digitizer/Singles/upholder/setUphold 750 keV']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestDeadTime(unittest.TestCase):
    def test_render(self):
        class dummyVolume:
            name = 'block'
        ddt = DeadTime(dummyVolume(), 3000)
        singles = Singles([ddt])
        to_compare = [ddt.render(),
                      '/gate/digitizer/Singles/insert deadtime\n/gate/digitizer/Singles/deadtime/setDeadTime 3000 ns\n/gate/digitizer/Singles/deadtime/chooseDTVolume block']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestCoincidenceSorter(unittest.TestCase):
    def test_render(self):
        cs = CoincidenceSorter(window=10, offset=0)
        to_compare = [cs.render(),
                      '/gate/digitizer/Coincidences/setWindow 10  ns\n/gate/digitizer/Coincidences/setOffset 0  ns']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)

    def test_render_add_new(self):
        cs = CoincidenceSorter(window=10, offset=500,
                               name='delay', define_name=True)
        to_compare = [cs.render(),
                      '/gate/digitizer/name delay\n/gate/digitizer/insert coincidenceSorter\n/gate/digitizer/delay/setWindow 10  ns\n/gate/digitizer/delay/setOffset 500  ns']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)


class TestCoincidencesChain(unittest.TestCase):
    def test_render(self):
        cs0 = CoincidenceSorter(window=10, offset=0)
        cs1 = CoincidenceSorter(window=10, offset=500,
                                name='delay', define_name=True)
        cc = CoincidencesChain([cs0, cs1], name='finalcoin', )
        to_compare = [cc.render(),
                      '/gate/digitizer/name finalcoin\n/gate/digitizer/insert coincidenceChain\n/gate/digitizer/finalcoin/addInputName Coincidences\n/gate/digitizer/finalcoin/addInputName delay\n/gate/digitizer/finalcoin/usePriority true']
        to_compare = [ignore_empty_newlines(s) for s in to_compare]
        self.assertEqual(*to_compare)
