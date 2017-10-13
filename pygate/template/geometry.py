# _*_ coding: utf-8 _*_
from math import pi
from .digitizer import AttrPair
import yaml


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getMacStr(self):
        fmt1 = r' {0}    {1}    {2}'
        return fmt1.format(self.x, self.y, self.z)


class Volume:
    shapeList = ['box', 'cylinder', 'sphere', 'patch']

    def __init__(self, shapeType, name, material=None, mother=None, position=None):
        if shapeType in Volume.shapeList:
            self.shapeType = shapeType
        else:
            print("invalid shape type: %s \n", shapeType)
        if mother is None:
            self.mother = 'world'
        else:
            self.mother = mother
        if material is None:
            self.material = 'Air'
        else:
            self.material = material

        self.name = name
        self.position = position
        self.attrList = []
        self.childList = []

    def makeAttrList(self):
        nameFmt = r"/gate/{0}/daughters/name {1}" + "\n"
        insertFmt = r"/gate/{0}/daughters/insert {1}" + "\n"
        posFmt = self.getMeStr() + r"/setTranslation {0}  mm" + "\n"
        matFmt = self.getMeStr() + r"/setMaterial {0}" + "\n"
        self.addAttr(
            AttrPair(self.mother, nameFmt.format(self.mother, self.name)))
        self.addAttr(AttrPair(self.mother, insertFmt.format(
            self.mother, self.shapeType)))
        if self.position is not None:
            self.addAttr(AttrPair(self.position, posFmt.format(self.position.getMacStr())))
        self.addAttr(AttrPair(self.material, matFmt.format(self.material)))

    def addChild(self, child):
        child.mother = self.name
        self.childList.append(child)

    def addAttr(self, attrItem):
        self.attrList.append(attrItem)

    def getMacStr(self):
        self.makeAttrList()
        mac = ""
        for item in self.attrList:
            if item.value is not None:
                mac += item.fmtstr
        for item in self.childList:
            mac += item.getMacStr()
        return mac

    def getMeStr(self):
        fmt = r"/gate/{0}"
        return fmt.format(self.name)


class Box(Volume):
    def __init__(self,  name, mother = None, position=None, material=None, size=None):
        super(Box, self).__init__(shapeType='box', mother=mother,
                                  name=name, position=position, material=material)
        if size is None:
            print("no box size in Box: %s", self.name)
        else:
            self.size = size

    def makeAttrList(self):
        super(Box, self).makeAttrList()
        sizeFmt = self.getMeStr() + r"/setXLength {0} mm" + "\n" + self.getMeStr(
        ) + r"/setYLength {1} mm" + "\n" + self.getMeStr() + r"/setZLength {2} mm" + "\n"
        self.addAttr(AttrPair(self.size, sizeFmt.format(
            self.size.x, self.size.y, self.size.z)))


class Cylinder(Volume):
    def __init__(self, name, Rmax,mother = None, Height=None, position=None, material=None,
                 Rmin=None, PhiStart=None, DeltaPhi=None):
        super(Cylinder, self).__init__(shapeType='cylinder',
                                       mother=mother, name=name, position=position, material=material)
        self.Rmin = Rmin
        self.Rmax = Rmax
        self.Height = Height
        self.PhiStart = PhiStart
        self.DeltaPhi = DeltaPhi

    def makeAttrList(self):
        super(Cylinder, self).makeAttrList()
        fmtRmin = self.getMeStr() + r"/setRmin {0} mm" + "\n"
        fmtRmax = self.getMeStr() + r"/setRmax {0} mm" + "\n"
        fmtHeight = self.getMeStr() + r"/setHeight {0} mm" + "\n"
        fmtPhiStart = self.getMeStr() + r"/setPhiStart {0}  deg" + "\n"
        fmtDeltaPhi = self.getMeStr() + r"/setDeltaPhi {0}  deg" + "\n"

        self.addAttr(AttrPair(self.Rmin, fmtRmin.format(self.Rmin)))
        self.addAttr(AttrPair(self.Rmax, fmtRmax.format(self.Rmax)))
        self.addAttr(AttrPair(self.Height, fmtHeight.format(self.Height)))
        self.addAttr(
            AttrPair(self.PhiStart, fmtPhiStart.format(self.PhiStart)))
        self.addAttr(
            AttrPair(self.DeltaPhi, fmtDeltaPhi.format(self.DeltaPhi)))


class Sphere(Volume):
    def __init__(self, name, Rmax, mother = None, position=None, material=None,
                 Rmin=None, PhiStart=None, DeltaPhi=None, ThetaStart=None, DeltaTheta=None):
        super(Sphere, self).__init__(shapeType='sphere',
                                     mother=mother, name=name, position=position, material=material)
        self.Rmin = Rmin
        self.Rmax = Rmax
        self.PhiStart = PhiStart
        self.DeltaPhi = DeltaPhi
        self.ThetaStart = ThetaStart
        self.DeltaTheta = DeltaTheta

    def makeAttrList(self):
        super(Sphere, self).makeAttrList()
        fmtRmin = r"/setRmin {0} mm" + "\n"
        fmtRmax = r"/setRmax {0} mm" + "\n"
        fmtPhiStart = r"/setPhiStart {0}  deg" + "\n"
        fmtDeltaPhi = r"/setDeltaPhi {0}  deg" + "\n"
        fmtThetaStart = r"/setThetaStart {0}  deg" + "\n"
        fmtDeltaTheta = r"/setDeltaTheta {0}  deg" + "\n"

        self.addAttr(AttrPair(self.Rmin, fmtRmin.format(self.Rmin)))
        self.addAttr(AttrPair(self.Rmax, fmtRmax.format(self.Rmax)))
        self.addAttr(
            AttrPair(self.PhiStart, fmtPhiStart.format(self.PhiStart)))
        self.addAttr(
            AttrPair(self.DeltaPhi, fmtDeltaPhi.format(self.DeltaPhi)))
        self.addAttr(AttrPair(self.ThetaStart,
                              fmtThetaStart.format(self.ThetaStart)))
        self.addAttr(AttrPair(self.DeltaTheta,
                              fmtDeltaTheta.format(self.DeltaTheta)))


class Repeater:
    def __init__(self, volume):
        self.volume = volume
    def getMacStr(self):
        pass


class RingRepeater(Repeater):
    def __init__(self, volume, number):
        super(RingRepeater, self).__init__(volume)
        self.number = number

    def getMacStr(self):
        fmt1 = r"/gate/{0}/repeaters/insert ring " + "\n"
        fmt2 = r"/gate/{0}/ring/setRepeatNumber {1}" + "\n"

        return(fmt1.format(self.volume)
               + fmt2.format(self.volume, self.number))


class LinearRepeater(Repeater):
    def __init__(self, volume, number, repeatVector):
        super(LinearRepeater, self).__init__(volume)
        self.number = number
        self.repeatVector = repeatVector

    def getMacStr(self):
        fmt1 = r"/gate/{0}/repeaters/insert linear " + "\n"
        fmt2 = r"/gate/{0}/linear/setRepeatNumber {1}" + " \n"
        fmt3 = r"/gate/{0}/linear/setRepeatVector {1}" + " \n"
        return (fmt1.format(self.volume) +
                fmt2.format(self.volume, self.number) +
                fmt3.format(self.volume, self.repeatVector))


class CubicRepeater(Repeater):
    def __init__(self, volume, scale, repeatVector):
        super(CubicRepeater, self).__init__(volume)
        self.scale = scale
        self.repeatVector = repeatVector

    def getMacStr(self):
        fmt1 = r"/gate/{0}/repeaters/insert cubicArray" + "\n"
        fmt2 = r"/gate/{0}/cubicArray/setRepeatNumber X   {1}" + " \n"
        fmt3 = r"/gate/{0}/cubicArray/setRepeatNumber Y   {1}" + " \n"
        fmt4 = r"/gate/{0}/cubicArray/setRepeatNumber Z   {1}" + " \n"
        fmt5 = r"/gate/{0}/cubicArray/setRepeatVecter {1}  mm" + " \n"

        return (fmt1.format(self.volume) +
                fmt2.format(self.volume, self.scale.x) +
                fmt3.format(self.volume, self.scale.y) +
                fmt4.format(self.volume, self.scale.z) +
                fmt5.format(self.volume, self.repeatVector.getMacStr())
                )


# if __name__ == '__main__':
#     c1 = Cylinder(mother='world', name='c1', Rmax = 30, Height = 30)
#     b1 = Box(mother = c1.name, name = 'b1', size=  Vec3(5,5,5))
#     rr = RingRepeater(volume = b1.name,number = 10)
#     c1.addChild(b1)
    
#     b2 = Box(mother = b1.name, name = 'b2',size = Vec3(2,2,2))
#     cr = CubicRepeater(volume = b2.name,scale = Vec3(2,2,2), repeatVector = Vec3(2.1,2.1,2.1))

#     b1.addChild(b2)
    

#     print(c1.getMacStr())
#     with open('geo.yml', 'w') as fout:
#         yaml.dump(b1, fout)
