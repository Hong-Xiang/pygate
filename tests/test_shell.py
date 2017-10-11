import unittest
from ruamel.yaml import YAML
from fs.memoryfs import MemoryFS
yaml = YAML()
from pygate import shell


class TestShellScript(unittest.TestCase):
    def test_shell_run(self):
        s = """#Config of tasks:
- name: Gate
  payloads:
    filename: some.mac
- name: root
  payloads:
    filename: some_analysis.C
- name: hadd
  payloads:
    target: result.root
    filenames:
        - sub0/result.root
        - sub1/result.root
"""
        expected = """#!/usr/bin/zsh
#SBATCH -o %J.out
#SBATCH -e %J.err
source ~/.zshrc
hostname
date
Gate some.mac
root -q -b some_analysis.C
hadd result.root sub0/result.root sub1/result.root
date

"""
        tasks = yaml.load(s)
        with MemoryFS() as fs:
            with fs.open('run.sh', 'w') as fout:
                s = shell.ShellScript(fout, tasks=tasks)
                s.dump()
            with fs.open('run.sh') as fin:
                result = fin.read()
        self.assertEqual(result, expected)
