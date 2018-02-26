from .base import ObjectWithTemplate
from .geometry import Volume
from .system import Systems
from typing import Tuple


class Camera(ObjectWithTemplate):
    template = 'camera'

    def __init__(self,
                 world: Volume,
                 system: Systems,
                 sensitive_detectors: Tuple[Volume]=tuple()):
        self.world = world
        self.system = system
        self.sds = sensitive_detectors
