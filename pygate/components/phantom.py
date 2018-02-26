from .base import ObjectWithTemplate
from .geometry import Volume
from typing import Tuple


class Phantom(ObjectWithTemplate):
    template = 'phantom'

    def __init__(self, sensitive_detectors: Tuple[Volume]=())
        self.sds = sensitive_detectors
