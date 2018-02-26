from typing import List
from .base import ObjectWithTemplate
from .utils import Vec3


class Source(ObjectWithTemplate):
    template = 'source/source'

    def __init__(self, name,
                 particle=None, activity=None, angle=None,
                 shape=None, position: Vec3=None):
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
        self.position = position

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

    def is_voxelized(self):
        return isinstance(self.shape, Voxelized)


class Particle(ObjectWithTemplate):
    template = 'source/particle/particle'
    particle_type = None

    def bind_source(self, source):
        self.src = source
        return self

    def __init__(self, unstable=None, halflife=None):
        self.scr = None
        self.unstable = unstable
        self.halflife = halflife


class ParticlePositron(Particle):
    template = 'source/particle/positron'
    particle_type = 'e+'

    def __init__(self, unstable=True, halflife=6586):
        super().__init__(unstable, halflife)


class ParticleGamma(Particle):
    template = 'source/particle/gamma'
    particle_type = 'gamma'

    def __init__(self,
                 unstable=True, halflife=6586.2,
                 monoenergy=511, back2back=True):
        super().__init__(unstable, halflife)
        self.back2back = back2back
        self.monoenergy = monoenergy


class Angular(ObjectWithTemplate):
    template = 'source/angular/angular'
    ang_type = None


class AngularISO(Angular):
    template = 'source/angular/iso'
    ang_type = 'iso'

    def __init__(self, ang=[0, 180, 0, 360]):
        self.ang = ang


class Shape(ObjectWithTemplate):
    template = 'source/shape/shape'
    shape = None

    def __init__(self, dimension):
        self.dimension = dimension


class ShapePlane(Shape):
    def __init__(self):
        super().__init__(dimension='Plane')


class ShapeSurfaceOrVolume(Shape):
    def __init__(self, dimension):
        if not dimension in ('Surface', 'Volume'):
            raise ValueError(
                'Invalid dimension {} for {}.'.format(dimension, __class__))
        super().__init__(dimension=dimension)


class Voxelized(Shape):
    template = 'source/shape/voxelized'
    shape = 'Voxelized'

    def __init__(self, read_table, read_file,
                 reader='interfile', translator='range',
                 position=None):
        self.read_table = read_table
        self.read_file = read_file
        self.reader = reader
        self.translator = translator
        self.position = position


class Cylinder(ShapeSurfaceOrVolume):
    template = 'source/shape/cylinder'
    shape = 'Cylinder'

    def __init__(self, radius, halfz, dimension):
        super().__init__(dimension)
        self.radius = radius
        self.halfz = halfz


class Sphere(Shape):
    template = 'source/shape/sphere'
    shape = 'Sphere'

    def __init__(self, radius, dimension):
        super().__init__(dimension)
        self.radius = radius


class Ellipsoid(Shape):
    template = 'source/shape/ellipsoid'
    shape = 'Ellipsoid'

    def __init__(self, half_size: Vec3, dimension):
        super().__init__(dimension)
        self.half_size = half_size


class Circle(ShapePlane):
    template = 'source/shape/circle'
    shape = 'Circle'

    def __init__(self, radius):
        super().__init__()
        self.radius = radius


class Annulus(ShapePlane):
    template = 'source/shape/annulus'
    shape = 'Annulus'

    def __init__(self, radius0, radius):
        super().__init__()
        self.radius = radius
        self.radius0 = radius0


class Ellipse(ShapePlane):
    template = 'source/shape/ellipse'
    shape = 'Ellipse'

    def __init__(self, half_size):
        super().__init__()
        self.half_size = half_size


class Rectangle(ShapePlane):
    template = 'source/shape/rectangle'
    shape = 'Rectangle'

    def __init__(self, half_size):
        super().__init__()
        self.half_size = half_size


class SourceList(ObjectWithTemplate):
    template = 'source/source_list'

    def __init__(self, sources: List[Source]):
        self.sources = sources
