# _*_ coding: utf-8 _*_
from math import pi
import yaml

from .base import ObjectWithTemplate


class Vec3(ObjectWithTemplate):
    template = 'vec3'

    def __init__(self, x, y, z, unit='mm'):
        self.x = x
        self.y = y
        self.z = z
        self.unit = unit


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

    def add_child(self, child):
        child.mother = self.name
        self.children.append(child)
        return child


class Box(Volume):
    shape_type = 'box'
    template = 'box'

    def __init__(self, name, size, material=None, mother=None, position=None, unit=None):
        super(Box, self).__init__(name, material, mother, position, unit)
        self.size = size


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


class ImageRegularParamerisedVolume(Volume):
    template = 'image_volume'
    shape_type = 'ImageRegularParametrisedVolume'

    def __init__(self,  name, image_file, range_file,
                 material=None, mother=None, position=None, unit=None):
        super().__init__(name, material, mother, position, unit)
        self.image_file = image_file
        self.range_file = range_file


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


class RepeaterLinear(Repeater):
    template = 'repeater_linear'
    repeater_type = 'linear'

    def __init__(self, volume, number, repeat_vector):
        super().__init__(volume)
        self.n = number
        self.rv = repeat_vector


class RepeaterCubic(Repeater):
    template = 'repeater_cubic'
    repeater_type = 'cubicArray'

    def __init__(self, volume, scale: Vec3, repeat_vector: Vec3):
        super().__init__(volume)
        self.scale = scale
        self.rv = repeat_vector
