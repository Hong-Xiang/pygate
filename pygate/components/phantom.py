from .base import ObjectWithTemplate
from .geometry import Volume
from .geometry.camera.system import System
from typing import Tuple


class Phantom(ObjectWithTemplate):
    template = 'phantom'

    def __init__(self,
                 sensitive_phantoms: Tuple[Volume]=tuple()):
        self.sds = sensitive_phantoms