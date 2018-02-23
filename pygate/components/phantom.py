from . import geometry
import yaml


class Phantom:
    def __init__(self,name):
        self.name = name
        self.geoList = []
        self.phantomSDList = []

    def addGeo(self,item):
        self.geoList.append(item)
    def addPhantomSD(self,item):
        self.phantomSDList.append(item.name)
    def getMacStr(self):
        mac =""
        for item in self.geoList:
            mac += item.getMacStr()
        mac += self.getSDMacStr()

        return mac
    def getSDMacStr(self):
        mac = ""
        fmt = r"/gate/{0}/attachPhantomSD" + "\n"
        for item in self.phantomSDList:
            mac += fmt.format(item)
        return mac



# if __name__ == '__main__':
#     c1  = geometry.Cylinder(mother = 'world', name = 'NemaCylinder', Rmax = 82, Rmin = 56, Height = 5)
#     # print (b1.getMacStr())
#     b1 = geometry.Box(mother = c1.name, name = 'block', position = geometry.Vec3(66.5, 0.0, 0.0), size = geometry.Vec3(20,44,5))
#     c1.addChild(b1)

#     phantom = Phantom(name = 'phantom1')
#     phantom.addGeo(c1)
#     phantom.addPhantomSD(b1)

#     # print(phantom.getMacStr())

# with open('phantom.yml', 'w') as fout:
#     yaml.dump(phantom, fout)
