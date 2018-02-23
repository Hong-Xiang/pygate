from . import geometry
import yaml
from .digitizer import AttrPair


class Camera:
    def __init__(self, name, system):
        self.name = name
        self.system = system
        self.geoList = []
        self.crystalSDList = []

    def addGeo(self, item):
        self.geoList.append(item)

    def addCrystalSD(self, item):
        self.crystalSDList.append(item)

    def getMacStr(self):
        mac = ""
        for item in self.geoList:
            mac += item.getMacStr()
        mac += self.system.getMacStr()
        mac += self.getSDMacStr()

        return mac

    def getSDMacStr(self):
        mac = ""
        fmt = r"/gate/{0}/attachCrystalSD" + "\n"
        for item in self.crystalSDList:
            mac += fmt.format(item)
        return mac


class Systems:
    sysList = ["PETscanner", "cylindricalPET", "ecat", "MultiPatchPET"]

    def __init__(self, name):
        if name in Systems.sysList:
            self.name = name
        else:
            print("invalid system name!  Systems:__init__() \n", name)
        self.levelList = []
        self.attachList = []

    def attachSystem(self, itemList):
        self.attachList = itemList

    def getMacStr(self):
        mac = ""
        fmt = r"/gate/systems/{0}/{1}/attach {2}" + "\n"
        # for i in range(len(self.attachList)):
        for l, a in zip(self.levelList, self.attachList):
            # mac += fmt.format(self.name, self.levelList[i], self.attachList[i])
            if a == 'void':
                mac = mac
            else:
                mac += fmt.format(self.name, l, a)
        return mac


class PETscanner(Systems):
    # levelList = ['level{0}'.format(i) for i in range(1, 6)]

    def __init__(self):
        super(PETscanner, self).__init__(name='PETscaner')
        self.levelList.append('level1')
        self.levelList.append('level2')
        self.levelList.append('level3')
        self.levelList.append('level4')
        self.levelList.append('level5')


class Ecat(Systems):
    # levelList = ['block', 'crystal']

    def __init__(self):
        super(Ecat, self).__init__(name='ecat')
        self.levelList.append('block')
        self.levelList.append('crystal')


class CylindericalPET(Systems):
    def __init__(self):
        super(CylindericalPET, self).__init__(name='cylindricalPET')
        self.levelList.append('rsector')
        self.levelList.append('module')
        self.levelList.append('submodule')
        self.levelList.append('crystal')
        self.levelList.append('layer0')
        self.levelList.append('layer1')
        self.levelList.append('layer2')
        self.levelList.append('layer3')


# if __name__ == '__main__':
#     #   an Ecat scanner case

#     # print (camera1.getMacStr())
#     with open('camera.yml', 'w') as fout:
#         yaml.dump(camera1, fout)
