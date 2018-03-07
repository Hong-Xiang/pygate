from ..base import ObjectWithTemplate
from .volume import Volume
from typing import Tuple
from .surface import Surface


class GeometryPreInitialise(ObjectWithTemplate):
    template = 'geometry/geometry_pre_init'

    def __init__(self, world: Volume,
                 camera, phantom):
        self.world = world
        self.camera = camera
        self.phantom = phantom


class GeometryPostInitialise(ObjectWithTemplate):
    template = 'geometry/geometry_post_init'

    def __init__(self, surfaces):
        self.surfaces = surfaces


class Geometry:
    def __init__(self, world: Volume,
                 camera, phantom,
                 surfaces: Tuple[Surface]=()):
        self.geometry_pre_initialise = GeometryPreInitialise(world,
                                                             camera, phantom)
        self.geometry_post_initialise = GeometryPostInitialise(surfaces)

    def render_pre(self):
        return self.geometry_pre_initialise.render()

    def render_post(self):
        return self.geometry_post_initialise.render()
