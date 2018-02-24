import unittest
from pygate.components.source import *


class TestParticlePositron(unittest.TestCase):
    def test_render(self):
        p = ParticlePositron()
        src = Source('src', particle=p)
        self.assertEqual(p.render(),
                         '/gate/source/src/gps/particle e+ \n/gate/source/src/gps/energytype Fluor18\n/gate/source/src/setForcedUnstableFlag true\n/gate/source/src/setForcedHalfLife 6586 s\n')


class TestAngularISO(unittest.TestCase):
    def test_render(self):
        a = AngularISO()
        src = Source('src', angle=a)
        self.assertEqual(a.render(),
                         '/gate/source/src/gps/angtype iso\n/gate/source/src/gps/mintheta 0 deg \n/gate/source/src/gps/maxtheta 180 deg\n/gate/source/src/gps/minphi   0 deg\n/gate/source/src/gps/maxphi   360 deg\n')
