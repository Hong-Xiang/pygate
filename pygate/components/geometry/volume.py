# _*_ coding: utf-8 _*_
from math import pi
import yaml
from dxl.shape.data import Box as Box_from_shape, CartesianRepeater
#from dxl.shape.data.group import CartesianRepeater 
from ..base import ObjectWithTemplate
from ..utils import Vec3
from typing import Tuple




class Repeater(ObjectWithTemplate):
    template = 'geometry/volume/repeater/repeater'
    repeater_type = None


class RepeaterRing(Repeater):
    template = 'geometry/volume/repeater/ring'
    repeater_type = 'ring'

    def __init__(self, number = None, ring_repeater = None):
        super().__init__()
        self.ring_repeater = ring_repeater 
        if self.ring_repeater is None:
            self.number = number
        else:
            self.number = self.ring_repeater.num

class RepeaterLinear(Repeater):
    template = 'geometry/volume/repeater/linear'
    repeater_type = 'linear'

    def __init__(self, number = None, steps = None, linear_repeater = None, unit = None):
        super().__init__()
        self.linear_repeater = linear_repeater
        self.unit = unit or 'mm'
        if self.linear_repeater is None:
            self.number = number
            self.steps = steps
        else:
            #steps_x, steps_y, steps_z = self.linear_repeater.steps
            self.number = max(self.linear_repeater.grids)
            self.steps = Vec3(*self.linear_repeater.steps, self.unit)

class RepeaterCubic(Repeater):
    template = 'geometry/volume/repeater/cubic'
    repeater_type = 'cubicArray'

    def __init__(self, grids = None, steps = None, cartesian_repeater = None, unit = None):
        super().__init__()
        self.cartesian_repeater = cartesian_repeater
        self.unit = unit or 'mm'
        if cartesian_repeater is None:
            self.grids = grids
            self.steps = steps
        else:
            # grids_x, grids_y, grids_z = self.cartesian_repeater.grids
            # steps_x, steps_y, steps_z = self.cartesian_repeater.steps
            self.grids = Vec3(*self.cartesian_repeater.grids, None)
            self.steps = Vec3(*self.cartesian_repeater.steps, self.unit)

        if self.steps.unit is None:
            self.steps.unit = self.unit


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

    def __init__(self, name, size=None, material=None, mother=None, position=None, unit=None, repeaters: Repeater=None, box_from_shape=None):
        super().__init__(name, material, mother, position, unit, repeaters)
        self.box_from_shape = box_from_shape
        if box_from_shape is None:
            self.size = size
            self.position = position
        else:
            shape_x,shape_y,shape_z = self.box_from_shape.shape
            origin_x,origin_y,origin_z = self.box_from_shape.origin
            self.size = Vec3(shape_x, shape_y, shape_z, self.unit)
            self.position = Vec3(origin_x, origin_y, origin_z, self.unit)
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





