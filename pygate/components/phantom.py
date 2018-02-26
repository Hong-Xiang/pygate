from .base import ObjectWithTemplate
from .geometry import Volume
from .system import System
from typing import Tuple


class Phantom(ObjectWithTemplate):
    template = 'phantom'

    def __init__(self,
                 world: Volume,
                 sensitive_phantoms: Tuple[Volume]=tuple()):
        self.world = world
        self.sds = sensitive_phantoms