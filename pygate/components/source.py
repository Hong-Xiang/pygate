from .digitizer import AttrPair
from .geometry import Vec3
import yaml


class SrcModule:
    def __init__(self, srcName=None):
        self.srcName = srcName
        self.attrList = []

    def getMacStr(self):
        self.makeAttrList()
        mac = ""
        for item in self.attrList:
            if item.value is not None:
                mac += item.fmtstr
        return mac

    def makeAttrList(self):
        pass

    def addAttr(self, attrItem):
        self.attrList.append(attrItem)


from .base import ObjectWithTemplate
from .geometry import Vec3

class Source(ObjectWithTemplate):
    template = 'source'

    def __init__(self, name, 
                 particle=None, activity=None, angle=None,
                 shape=None, placement:Vec3=None):
        """
        Args:
            activity: str | int | float | list | tuple:
                str: directly attached
                int, float: add default unit becquerel
                list, tuple: [0]: value, [1]: unit
        """
        self.name = name
        self.particle = self.bind(particle)
        self.angle = self.bind(angle)
        self.shape = self.bind(shape)
        self.activity = self.unified_activity(activity)

    def unified_activity(self, activity):
        if activity is None:
            return None
        if isinstance(activity, str):
            return activity
        if isinstance(activity, (int, float)):
            unit = 'becquerel'
        if isinstance(activity, (list, tuple)):
            unit = activity[1]
            activity = activity[0]
            if unit.lower() in ['bq']:
                unit = 'becquerel'
        return "{} {}".format(activity, unit)

    def bind(self, obj):
        if obj is not None:
            obj.src = self
        return obj

class Particle(ObjectWithTemplate):
    template = 'source_particle'
    particle_type = None

    def bind_source(self, source):
        self.src = source
        return self

    def __init__(self, unstable=None, halflife=None):
        self.scr = None
        self.unstable = unstable
        self.halflife = halflife

class ParticlePositron(Particle):
    template = 'source_particle_positron'
    particle_type = 'e+'

    def __init__(self, unstable=True, halflife=6586):
        super().__init__(unstable, halflife)


class ParticleGamma(Particle):
    template = 'source_particle_gamma'
    particle_type = 'gamma'

    def __init__(self,
                 unstable=True, halflife=6586.2,
                 monoenery=511, back2back=True):
        super().__init__(unstable, halflife)
        self.back2back = back2back
        self.monoenergy = monoenergy

    # def makeAttrList(self):
    #     if self.particleType == 'positron':
    #         fmt = (r"/gate/source/{0}/gps/particle e+ " + "\n" +
    #                r"/gate/source/{0}/gps/energytype Fluor18" + "\n" +
    #                r"/gate/source/{0}/setForcedUnstableFlag true" + "\n" +
    #                r"/gate/source/{0}/setForcedHalfLife 6586 s" + "\n")
    #         self.addAttr(AttrPair(self.particleType, fmt.format(self.srcName)))
    #     elif self.particleType == 'gamma':
    #         fmt = (r"/gate/source/{0}/setType backtoback" + "\n" +
    #                r"/gate/source/{0}/gps/particle gamma " + "\n" +
    #                r"/gate/source/{0}/gps/monoenergy 511 keV" + "\n" +
    #                r"/gate/source/{0}/setForcedUnstableFlag true" + "\n" +
    #                r"/gate/source/{0}/setForcedHalfLife 6586.2 s" + "\n")
    #         self.addAttr(AttrPair(self.particleType, fmt.format(self.srcName)))
    #     else:
    #         print("invalid particle type in Particle:makeAttrList() \n")


# class Activity(SrcModule):
#     def __init__(self, srcName=None, activity=None):
#         super(Activity, self).__init__(srcName=srcName)
#         self.activity = activity

#     def makeAttrList(self):
#         fmt = r"/gate/source/{0}/setActivity {1}  becquerel" + "\n"
#         self.addAttr(AttrPair(self.activity, fmt.format(
#             self.srcName, self.activity)))
class Shape(ObjectWithTemplate):
    template = 'source_shape'

class Angular(ObjectWithTemplate):
    template = 'source_angular'
    ang_type = None

class AngularISO(Angular):
    template = 'source_angular_iso'
    ang_type = 'iso'
    def __init__(self, ang=[0, 180, 0, 360]):
        self.ang = ang

class Voxelized(Shape):
    def __init__(self, readtable, readfile, shape='Voxelized', reader='interfile', translator='range', srcName=None, position=None):
        super(Voxelized, self).__init__(srcName=srcName)
        self.shape = shape
        self.reader = reader
        self.translator = translator
        self.readtable = readtable
        self.readfile = readfile
        self.position = position

    def makeAttrList(self):
        fmt = (r"/gate/source/{0}/reader/insert {1}" + "\n" +
               r"/gate/source/{0}/{1}Reader/translator/insert {2} " + "\n" +
               r"/gate/source/{0}/{1}Reader/{2}Translator/readTable {3}" + "\n" +
               r"/gate/source/{0}/{1}Reader/readFile  {4}" + "\n" +
               r"/gate/source/{0}/setPosition  {5}  mm" + "\n")
        self.addAttr(AttrPair(self.shape, fmt.format(self.srcName, self.reader,
                                                     self.translator, self.readtable, self.readfile, self.position.getMacStr())))


class Shape(SrcModule):
    PlaneList = ['Circle', 'Annulus', 'Ellpsoid', 'Square', 'Rectangle']
    VolumeList = ['Sphere', 'Ellipsoid', 'Cylinder', 'Para']

    def __init__(self, dimension, shape, srcName=None):
        super(Shape, self).__init__(srcName=srcName)
        if dimension is 'Plane':
            if shape in Shape.PlaneList:
                self.dimension = dimension
                self.shape = shape
        elif ((dimension is 'Surface') or (dimension is 'Volume')):
            if shape in Shape.VolumeList:
                self.dimension = dimension
                self.shape = shape
        else:
            pass

    def makeAttrList(self):
        fmt1 = r"/gate/source/{0}/gps/type {1}" + "\n"
        fmt2 = r"/gate/source/{0}/gps/shape {1}" + "\n"
        self.addAttr(AttrPair(self.dimension, fmt1.format(
            self.srcName, self.dimension)))
        self.addAttr(
            AttrPair(self.shape, fmt2.format(self.srcName, self.shape)))


class Cylinder(Shape):
    def __init__(self, radius, halfz, dimension, srcName=None):
        super(Cylinder, self).__init__(
            dimension=dimension, shape='Cylinder', srcName=srcName)
        self.radius = radius
        self.halfz = halfz

    def makeAttrList(self):
        super(Cylinder, self).makeAttrList()
        fmt1 = r"/gate/source/{0}/gps/radius {1} mm" + "\n"
        fmt2 = r"/gate/source/{0}/gps/halfz {1} mm" + "\n"
        self.addAttr(
            AttrPair(self.radius, fmt1.format(self.srcName, self.radius)))
        self.addAttr(
            AttrPair(self.halfz, fmt2.format(self.srcName, self.halfz)))


class Sphere(Shape):
    def __init__(self, radius, dimension, srcName=None):
        super(Sphere, self).__init__(
            dimension=dimension, shape='Sphere', srcName=srcName)
        self.radius = radius

    def makeAttrList(self):
        super(Sphere, self).makeAttrList()
        fmt1 = r"/gate/source/{0}/gps/radius {1} mm" + "\n"
        self.addAttr(
            AttrPair(self.radius, fmt1.format(self.srcName, self.radius)))


class Ellipsoid(Shape):
    def __init__(self, halfSize, dimension, srcName=None):
        super(Ellipsoid, self).__init__(
            dimension=dimension, shape='Ellipsoid', srcName=srcName)
        self.halfSize = halfSize

    def makeAttrList(self):
        super(Ellipsoid, self).makeAttrList()
        fmt1 = (r"/gate/source/{0}/gps/halfx {1} mm" + "\n" +
                r"/gate/source/{0}/gps/halfy {2} mm" + "\n" +
                r"/gate/source/{0}/gps/halfz {3} mm" + "\n")
        self.addAttr(AttrPair(self.halfSize, fmt1.format(
            self.srcName, self.halfSize[0], self.halfSize[1], self.halfSize[2])))


class Circle(Shape):
    def __init__(self, radius, srcName=None):
        super(Circle, self).__init__(
            dimension='Plane', shape='Circle', srcName=srcName)
        self.radius = radius

    def makeAttrList(self):
        super(Circle, self).makeAttrList()
        fmt1 = (r"/gate/source/{0}/gps/radius {1} mm" + "\n")
        self.addAttr(
            AttrPair(self.radius, fmt1.format(self.srcName, self.radius)))


class Annulus(Shape):
    def __init__(self, radius0, radius, srcName=None):
        super(Annulus, self).__init__(
            dimension='Plane', shape='Annulus', srcName=srcName)
        self.radius = radius
        self.radius0 = radius0

    def makeAttrList(self):
        super(Annulus, self).makeAttrList()
        fmt1 = (r"/gate/source/{0}/gps/radius0 {1} mm" + "\n")
        fmt2 = (r"/gate/source/{0}/gps/radius {1} mm" + "\n")
        self.addAttr(
            AttrPair(self.radius0, fmt1.format(self.srcName, self.radius0)))
        self.addAttr(
            AttrPair(self.radius, fmt2.format(self.srcName, self.radius)))


class Ellipse(Shape):
    def __init__(self, halfSize, srcName=None):
        super(Ellipse, self).__init__(
            dimension="Plane", shape='Ellipse', srcName=srcName)
        self.halfSize = halfSize

    def makeAttrList(self):
        super(Ellipse, self).makeAttrList()
        fmt1 = (r"/gate/source/{0}/gps/halfx {1} mm" + "\n" +
                r"/gate/source/{0}/gps/halfy {2} mm" + "\n")
        self.addAttr(AttrPair(self.halfSize, fmt1.format(
            self.srcName, self.halfSize[0], self.halfSize[1])))


class Rectangle(Shape):
    def __init__(self, halfSize, srcName=None):
        super(Rectangle, self).__init__(
            dimension="Plane", shape='Rectangle', srcName=srcName)
        self.halfSize = halfSize

    def makeAttrList(self):
        super(Rectangle, self).makeAttrList()
        fmt1 = (r"/gate/source/{0}/gps/halfx {1} mm" + "\n" +
                r"/gate/source/{0}/gps/halfy {2} mm" + "\n")
        self.addAttr(AttrPair(self.halfSize, fmt1.format(
            self.srcName, self.halfSize[0], self.halfSize[1])))


class Placement(SrcModule):
    def __init__(self, srcName=None, placement=None):
        super(Placement, self).__init__(srcName=srcName)
        self.placement = placement

    def makeAttrList(self):
        fmt = r"/gate/source/{0}/centre {1}  mm" + "\n"
        self.addAttr(AttrPair(self.placement, fmt.format(
            self.srcName, self.placement.getMacStr())))


class SrcItem:
    def __init__(self, name):
        self.srcModuleList = []
        self.name = name

    def addSrcModule(self, item):
        item.srcName = self.name
        self.srcModuleList.append(item)

    def getMacStr(self):
        mac = ""
        fmt = r"/gate/source/addSource {0}" + "\n"
        mac += fmt.format(self.name)
        for item in self.srcModuleList:
            mac += item.getMacStr()
        return mac


class VoxelizedSrcItem:
    def __init__(self, name):
        self.srcModuleList = []
        self.name = name

    def addSrcModule(self, item):
        item.srcName = self.name
        self.srcModuleList.append(item)

    def getMacStr(self):
        mac = ""
        fmt = r"/gate/source/addSource {0} voxel" + "\n"
        mac += fmt.format(self.name)
        for item in self.srcModuleList:
            mac += item.getMacStr()
        return mac


class SourceList(ObjectWithTemplate):
    template = 'source_list'

    def __init__(self, sources):
        self.sources = sources

    def getMacStr(self):
        mac = ""
        for item in self.srcItemList:
            mac += item.getMacStr()
        mac += r"/gate/source/list" + "\n"
        return mac


# if __name__ is "__main__":

#     src1 = SrcItem(name='src1')
#     src1.addSrcModule(Particle(paticleType='gamma'))
#     src1.addSrcModule(Angular(ang=[90, 90, 0, 360]))
#     # src1.addSrcModule(Rectangle(halfSize = [10,20]))
#     src1.addSrcModule(Cylinder(dimension = 'Volume',halfz = 10 , radius = 10))
#     src1.addSrcModule(Placement(placement=Vec3(10, 10, 10)))

#     src = Source()
#     src.addSourceItem(src1)

#     print(src.getMacStr())
# with open('source.yml', 'w') as fout:
#     yaml.dump(src, fout)
