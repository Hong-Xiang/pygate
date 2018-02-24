from .base import ObjectWithTemplate


class Systems(ObjectWithTemplate):
    template = 'system'
    name = None
    attach_systems = None

    def __init__(self):
        self.levels = self.attach_systems()
        self.levels = {k: self.levels[k]
                       for k in self.levels if self.levels[k] is not None}

    def attachSystem(self, itemList):
        self.attachList = itemList


class PETscanner(Systems):
    name = 'PETscanner'

    def __init__(self, level1, level2, level3, level4, level5):
        self.attach_systems = lambda: {
            'level1': level1,
            'level2': level2,
            'level3': level3,
            'level4': level4,
            'level5': level5
        }
        super().__init__()


class Ecat(Systems):
    name = 'ecat'

    def __init__(self, block=None, crystal=None):
        self.attach_systems = lambda:  {'block': block, 'crystal': crystal}
        super().__init__()


class CylindericalPET(Systems):
    name = 'cylindricalPET'

    def __init__(self,
                 rsector=None, module=None, submodule=None, crystal=None,
                 layer0=None, layer1=None, layer2=None, layer3=None):
        self.attach_systems = lambda: {
            'rsector': rsector,
            'module': module,
            'submodule': submodule,
            'crystal': crystal,
            'layer0': layer0,
            'layer1': layer1,
            'layer2': layer2,
            'layer3': layer3,
        }
        super().__init__()
