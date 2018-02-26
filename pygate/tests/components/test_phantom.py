import unittest

from pygate.components.phantom import Phantom


class TestPhantom(unittest.TestCase):
    def test_render(self):
        class DummyVolume:
            name = 'phantom'
        p = Phantom((DummyVolume,))
        self.assertEqual(p.render(),
                         '/gate/phantom/attachPhantomSD\n')
