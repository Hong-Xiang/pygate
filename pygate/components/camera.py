from . import geometry
import yaml
from .digitizer import AttrPair

# class Camera:
#     def __init__(self, name, system):
#         self.name = name
#         self.system = system
#         self.geoList = []
#         self.crystalSDList = []

#     def addGeo(self, item):
#         self.geoList.append(item)

#     def addCrystalSD(self, item):
#         self.crystalSDList.append(item)

#     def getMacStr(self):
#         mac = ""
#         for item in self.geoList:
#             mac += item.getMacStr()
#         mac += self.system.getMacStr()
#         mac += self.getSDMacStr()

#         return mac

#     def getSDMacStr(self):
#         mac = ""
#         fmt = r"/gate/{0}/attachCrystalSD" + "\n"
#         for item in self.crystalSDList:
#             mac += fmt.format(item)
#         return mac
