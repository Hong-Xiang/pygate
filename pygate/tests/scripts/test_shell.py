import unittest
from pygate.shell_scripts.shell import ScriptRun, GateSimulation, RootAnalysis


class TestScriptRun(unittest.TestCase):
    def test_render(self):
        sr = (ScriptRun('/hqlf/test/', (GateSimulation('main.mac'),), 8.0)
              .add_task(RootAnalysis('result.root')))
        self.assertEqual(sr.render(),
                         "#!/bin/bash\n\n#SBATCH -o %J.out\n#SBATCH -e %J.err\n#SBATCH -p cpu\n\nsource /hqlf/softwares/module/simu8.0.sh\necho 'Run on:' `hostname`\necho 'Start at: ' `date`\necho 'Start MC Simulation at: ' `date`\ncd /hqlf/test/\nGate main.mac\nroot -q -b result.root\necho 'Finish MC Simulation at: ' `date`\necho 'Finish at: ' `date`\n")

    def test_render_2(self):
        sr = (ScriptRun('/hqlf/test/')
              .add_task(GateSimulation('main.mac'))
              .add_task(RootAnalysis('result.root')))
        self.assertEqual(sr.render(),
                         "#!/bin/bash\n\n#SBATCH -o %J.out\n#SBATCH -e %J.err\n#SBATCH -p cpu\n\nsource /hqlf/softwares/module/simu8.0.sh\necho 'Run on:' `hostname`\necho 'Start at: ' `date`\necho 'Start MC Simulation at: ' `date`\ncd /hqlf/test/\nGate main.mac\nroot -q -b result.root\necho 'Finish MC Simulation at: ' `date`\necho 'Finish at: ' `date`\n")
