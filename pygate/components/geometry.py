# _*_ coding: utf-8 _*_
from math import pi
from .digitizer import AttrPair
import yaml

from .base import ObjectWithTemplate


class Vec3(ObjectWithTemplate):
    template = 'vec3'

    def __init__(self, x, y, z, unit='mm'):
        self.x = x
        self.y = y
        self.z = z
        self.unit = unit

    # def getMacStr(self):
    #     fmt1 = r' {0}    {1}    {2}'
    #     return fmt1.format(self.x, self.y, self.z)


class Volume(ObjectWithTemplate):
    shape_type = 'volume'
    template = 'volume'

    def __init__(self, name, material=None, mother=None, position=None, unit=None):
        self.mother = mother
        self.name = name
        self.material = material
        self.position = position
        self.unit = unit or 'mm'
        self.children = []
        self.attrList = []
        # self.childList = []

    # def makeAttrList(self):
    #     nameFmt = r"/gate/{0}/daughters/name {1}" + "\n"
    #     insertFmt = r"/gate/{0}/daughters/insert {1}" + "\n"
    #     posFmt = r"/gate/{0}/placement/setTranslation {1}  mm" + "\n"
    #     matFmt = r"/gate/{0}/setMaterial {1}" + "\n"
    #     self.addAttr(
    #         AttrPair(self.mother, nameFmt.format(self.mother, self.name)))
    #     self.addAttr(AttrPair(self.mother, insertFmt.format(
    #         self.mother, self.shapeType)))
    #     if self.position is not None:
    #         self.addAttr(
    #             AttrPair(self.position, posFmt.format(self.name, self.position.getMacStr())))
    #     if self.material is not None:
    #         self.addAttr(
    #             AttrPair(self.material, matFmt.format(self.name, self.material)))

    def add_child(self, child):
        child.mother = self.name
        self.children.append(child)
        return child

    def addAttr(self, attrItem):
        self.attrList.append(attrItem)

    def getMacStr(self):
        # self.makeAttrList()
        mac = ""
        for item in self.attrList:
            if item.value is not None:
                mac += item.fmtstr
        for item in self.childList:
            mac += item.getMacStr()
        return mac

    def getMeStr(self):
        fmt = r"/gate/{0}/geometry"
        return fmt.format(self.name)


class Box(Volume):
    shape_type = 'box'
    template = 'box'

    def __init__(self, name, size, material=None, mother=None, position=None, unit=None):
        super(Box, self).__init__(name, material, mother, position, unit)
        self.size = size

    # def makeAttrList(self):
    #     super(Box, self).makeAttrList()
    #     sizeFmt = self.getMeStr() + r"/setXLength {0} mm" + "\n" + self.getMeStr(
    #     ) + r"/setYLength {1} mm" + "\n" + self.getMeStr() + r"/setZLength {2} mm" + "\n"
    #     self.addAttr(AttrPair(self.size, sizeFmt.format(
    #         self.size.x, self.size.y, self.size.z)))


class Cylinder(Volume):
    shape_type = 'cylinder'
    template = 'cylinder'

    def __init__(self, name, rmax, rmin=None, height=None,
                 phi_start=None, delta_phi=None,
                 material=None, mother=None, position=None, unit=None):
        super().__init__(name, material, mother, position, unit)
        self.rmax = rmax
        self.rmin = rmin
        self.height = height
        self.phi_start = phi_start
        self.delta_phi = delta_phi

    # def makeAttrList(self):
    #     super(Cylinder, self).makeAttrList()
    #     fmtRmin = self.getMeStr() + r"/setRmin {0} mm" + "\n"
    #     fmtRmax = self.getMeStr() + r"/setRmax {0} mm" + "\n"
    #     fmtHeight = self.getMeStr() + r"/setHeight {0} mm" + "\n"
    #     fmtPhiStart = self.getMeStr() + r"/setPhiStart {0}  deg" + "\n"
    #     fmtDeltaPhi = self.getMeStr() + r"/setDeltaPhi {0}  deg" + "\n"

        # self.addAttr(AttrPair(self.Rmin, fmtRmin.format(self.Rmin)))
        # self.addAttr(AttrPair(self.Rmax, fmtRmax.format(self.Rmax)))
        # self.addAttr(AttrPair(self.Height, fmtHeight.format(self.Height)))
        # self.addAttr(
        #     AttrPair(self.PhiStart, fmtPhiStart.format(self.PhiStart)))
        # self.addAttr(
        #     AttrPair(self.DeltaPhi, fmtDeltaPhi.format(self.DeltaPhi)))


class Sphere(Volume):
    template = 'sphere'
    shape_type = 'sphere'

    def __init__(self, name, rmax, rmin=None, height=None,
                 phi_start=None, delta_phi=None,
                 theta_start=None, delta_theta=None,
                 material=None, mother=None, position=None, unit=None):
        super().__init__(name, material, mother, position, unit)
        self.rmax = rmax
        self.rmin = rmin
        self.height = height
        self.phi_start = phi_start
        self.delta_phi = delta_phi
        self.theta_start = theta_start
        self.delta_theta = delta_theta

    # def makeAttrList(self):
    #     super(Sphere, self).makeAttrList()
    #     fmtRmin = self.getMeStr() + r"/setRmin {0} mm" + "\n"
    #     fmtRmax = self.getMeStr() + r"/setRmax {0} mm" + "\n"
    #     fmtPhiStart = self.getMeStr() + r"/setPhiStart {0}  deg" + "\n"
    #     fmtDeltaPhi = self.getMeStr() + r"/setDeltaPhi {0}  deg" + "\n"
    #     fmtThetaStart = self.getMeStr() + r"/setThetaStart {0}  deg" + "\n"
    #     fmtDeltaTheta = self.getMeStr() + r"/setDeltaTheta {0}  deg" + "\n"

        # self.addAttr(AttrPair(self.Rmin, fmtRmin.format(self.Rmin)))
        # self.addAttr(AttrPair(self.Rmax, fmtRmax.format(self.Rmax)))
        # self.addAttr(
        #     AttrPair(self.PhiStart, fmtPhiStart.format(self.PhiStart)))
        # self.addAttr(
        #     AttrPair(self.DeltaPhi, fmtDeltaPhi.format(self.DeltaPhi)))
        # self.addAttr(AttrPair(self.ThetaStart,
        #                       fmtThetaStart.format(self.ThetaStart)))
        # self.addAttr(AttrPair(self.DeltaTheta,
        #                       fmtDeltaTheta.format(self.DeltaTheta)))


class ImageRegularParamerisedVolume(Volume):
    template = 'image_volume'
    shape_type = 'ImageRegularParametrisedVolume'

    def __init__(self,  name, image_file, range_file,
                 material=None, mother=None, position=None, unit=None):
        super().__init__(name, material, mother, position, unit)
        self.image_file = image_file
        self.range_file = range_file

    # def makeAttrList(self):
    #     super(ImageRegularParamerisedVolume, self).makeAttrList()
    #     ImageFileFmt = self.getMeStr() + r"/setImage {0} " + "\n"
    #     self.addAttr(
    #         AttrPair(self.imagefile, ImageFileFmt.format(self.imagefile)))
    #     RangeFileFmt = self.getMeStr() + r"/setRangeToMaterialFile {0} " + "\n"
    #     self.addAttr(
    #         AttrPair(self.rangefile, RangeFileFmt.format(self.rangefile)))


class Repeater(ObjectWithTemplate):
    template = 'repeater'
    repeater_type = None

    def __init__(self, volume):
        self.volume = volume


class RepeaterRing(Repeater):
    template = 'repeater_ring'
    repeater_type = 'ring'

    def __init__(self, volume, number):
        super().__init__(volume)
        self.n = number

    # def getMacStr(self):
    #     fmt1 = r"/gate/{0}/repeaters/insert ring " + "\n"
    #     fmt2 = r"/gate/{0}/ring/setRepeatNumber {1}" + "\n"

    #     return(fmt1.format(self.volume)
    #            + fmt2.format(self.volume, self.number))


class RepeaterLinear(Repeater):
    template = 'repeater_linear'
    repeater_type = 'linear'

    def __init__(self, volume, number, repeat_vector):
        super().__init__(volume)
        self.n = number
        self.rv = repeat_vector

    # def getMacStr(self):
    #     fmt1 = r"/gate/{0}/repeaters/insert linear " + "\n"
    #     fmt2 = r"/gate/{0}/linear/setRepeatNumber {1}" + " \n"
    #     fmt3 = r"/gate/{0}/linear/setRepeatVector {1}" + " \n"
    #     return (fmt1.format(self.volume) +
    #             fmt2.format(self.volume, self.number) +
    #             fmt3.format(self.volume, self.repeatVector))


class RepeaterCubic(Repeater):
    template = 'repeater_cubic'
    repeater_type = 'cubicArray'

    def __init__(self, volume, scale: Vec3, repeat_vector: Vec3):
        super().__init__(volume)
        self.scale = scale
        self.rv = repeat_vector

    # def getMacStr(self):
    #     fmt1 = r"/gate/{0}/repeaters/insert cubicArray" + "\n"
    #     fmt2 = r"/gate/{0}/cubicArray/setRepeatNumberX   {1}" + " \n"
    #     fmt3 = r"/gate/{0}/cubicArray/setRepeatNumberY   {1}" + " \n"
    #     fmt4 = r"/gate/{0}/cubicArray/setRepeatNumberZ   {1}" + " \n"
    #     fmt5 = r"/gate/{0}/cubicArray/setRepeatVector {1}  mm" + " \n"

    #     return (fmt1.format(self.volume) +
    #             fmt2.format(self.volume, self.scale.x) +
    #             fmt3.format(self.volume, self.scale.y) +
    #             fmt4.format(self.volume, self.scale.z) +
    #             fmt5.format(self.volume, self.repeatVector.getMacStr())
    #             )


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
