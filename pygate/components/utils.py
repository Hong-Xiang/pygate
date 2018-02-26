from .base import ObjectWithTemplate
class Vec3(ObjectWithTemplate):
    template = 'vec3'

    def __init__(self, x, y, z, unit=None):
        self.x = x
        self.y = y
        self.z = z
        self.unit = unit
