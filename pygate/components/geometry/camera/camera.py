from ...base import ObjectWithTemplate
from ..volume import Volume
from .system import System
from typing import Tuple


class Camera(ObjectWithTemplate):
    template = 'geometry/camera'

    def __init__(self,
                 system: System,
                 sensitive_detectors: Tuple[Volume]=()):
        self.system = system
        self.sds = sensitive_detectors
