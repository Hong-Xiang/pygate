from ..base import ObjectWithTemplate
from .volume import Volume
from typing import Tuple
from .surface import Surface


class Geometry(ObjectWithTemplate):
    template = 'geometry/geometry'

    def __init__(self, world: Volume,
                 camera, phantom,
                 surfaces: Tuple[Surface]=()):
        self.world = world
        self.camera = camera
        self.phantom = phantom
        self.surfaces = surfaces
