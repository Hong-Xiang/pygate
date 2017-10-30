import unittest
from ruamel.yaml import YAML
from fs.memoryfs import MemoryFS
from fs.osfs import OSFS
from dxpy.filesystem import Path
import jinja2
from pygate import shell


# class TestShellScript(unittest.TestCase):
#     def test_shell_bash(self):
#         from fs.osfs import OSFS
#         result = shell.make(OSFS('/tmp'), '/sub.1', 'map', [{'method':'Gate', 'filename': 'main.mac'}], shell='bash')
#         from pygate.utils import load_script
#         expect = load_script('map_bash_sample.sh')
#         self.assertEqual(result, expect)
        

