from ..base import ObjectWithTemplate
from .volume import Volume

class Surface(ObjectWithTemplate):

    template = 'geometry/surface'
    surface_type = None

    def __init__(self, name, base: Volume, insert: Volume):
        self.name = name
        self.base = base
        self.insert = insert


class SurfacePerfectAPD(Surface):
    surface_type = 'perfect_apd'

class SurfaceRoughTeflonWrapped(Surface):
    surface_type  = 'rough_teflon_wrapped'