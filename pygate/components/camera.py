from .base import ObjectWithTemplate
from .geometry import Volume
from .system import System
from typing import Tuple


class Camera(ObjectWithTemplate):
    template = 'camera'

    def __init__(self,
                 system: System,
                 sensitive_detectors: Tuple[Volume]=tuple()):
        self.system = system
        self.sds = sensitive_detectors
