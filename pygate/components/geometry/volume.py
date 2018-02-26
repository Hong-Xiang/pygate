# _*_ coding: utf-8 _*_
from math import pi
import yaml

from ..base import ObjectWithTemplate
from ..utils import Vec3
from typing import Tuple




class Repeater(ObjectWithTemplate):
    template = 'geometry/volume/repeater/repeater'
    repeater_type = None


class RepeaterRing(Repeater):
    template = 'geometry/volume/repeater/ring'
    repeater_type = 'ring'

    def __init__(self, number):
        super().__init__()
        self.n = number


class RepeaterLinear(Repeater):
    template = 'geometry/volume/repeater/linear'
    repeater_type = 'linear'

    def __init__(self, number, repeat_vector):
        super().__init__()
        self.n = number
        self.rv = repeat_vector


class RepeaterCubic(Repeater):
    template = 'geometry/volume/repeater/cubic'
    repeater_type = 'cubicArray'

    def __init__(self, scale: Vec3, repeat_vector: Vec3):
        super().__init__()
        self.scale = scale
        self.rv = repeat_vector


class Volume(ObjectWithTemplate):
    shape_type = 'volume'
    template = 'geometry/volume/volume'

    def __init__(self, name, material=None, mother=None, position=None, unit=None, repeaters: Repeater=None):
        self.mother = mother
        if self.mother is not None:
            self.mother.add_child(self)
        self.name = name
        self.material = material
        self.position = position
        self.unit = unit or 'mm'
        if self.position is not None and self.position.unit is None:
            self.position.unit = self.unit
        self.repeaters = repeaters or ()
        for r in self.repeaters:
            r.volume = self
        self.children = []

    def add_child(self, child):
        if not child.mother is self:
            raise ValueError(
                "Trying to ({}).add_child({}) with another mother {}.".format(self.name, child.name, child.mother.name))
        child.mother = self
        if not child in self.children:
            self.children.append(child)
        return child


class Box(Volume):
    shape_type = 'box'
    template = 'geometry/volume/box'

    def __init__(self, name, size, material=None, mother=None, position=None, unit=None, repeaters: Repeater=None):
        super().__init__(name, material, mother, position, unit, repeaters)
        self.size = size
        if self.size.unit is None:
            self.size.unit = self.unit


class Cylinder(Volume):
    shape_type = 'cylinder'
    template = 'geometry/volume/cylinder'

    def __init__(self, name, rmax, rmin=None, height=None,
                 phi_start=None, delta_phi=None,
                 material=None, mother=None, position=None, unit=None, repeaters: Repeater=None):
        super().__init__(name, material, mother, position, unit, repeaters)
        self.rmax = rmax
        self.rmin = rmin
        self.height = height
        self.phi_start = phi_start
        self.delta_phi = delta_phi


class Sphere(Volume):
    template = 'geometry/volume/sphere'
    shape_type = 'sphere'

    def __init__(self, name, rmax, rmin=None,
                 phi_start=None, delta_phi=None,
                 theta_start=None, delta_theta=None,
                 material=None, mother=None, position=None, unit=None, repeaters: Repeater=None):
        super().__init__(name, material, mother, position, unit, repeaters)
        self.rmax = rmax
        self.rmin = rmin
        self.phi_start = phi_start
        self.delta_phi = delta_phi
        self.theta_start = theta_start
        self.delta_theta = delta_theta


class ImageRegularParamerisedVolume(Volume):
    template = 'geometry/volume/image_volume'
    shape_type = 'ImageRegularParametrisedVolume'

    def __init__(self,  name, image_file, range_file,
                 material=None, mother=None, position=None, unit=None, repeaters: Repeater=None):
        super().__init__(name, material, mother, position, unit, repeaters)
        self.image_file = image_file
        self.range_file = range_file


class Patch(Volume):
    template = 'geometry/patch'
    shape_type = 'shape'

    def __init__(self, name, patch_file, material=None, mother=None, position=None, unit=None, repeater: Repeater = None):
        super().__init__(name, material, mother, position, unit, repeater)
        self.patch_file = patch_file





