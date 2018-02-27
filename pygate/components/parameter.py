from typing import List
from .base import ObjectWithTemplate


class Acquisition(ObjectWithTemplate):
    template = 'parameter/acquisition/acquisition'
    acquisition_type = None


class AcquisitionPrimaries(Acquisition):
    template = 'parameter/acquisition/primaries'
    acquisition_type = 'primaries'

    def __init__(self, number=10000):
        super().__init__()
        self.number = number


class AcquisitionPeriod(Acquisition):
    template = 'parameter/acquisition/period'
    acquisition_type = 'period'

    def __init__(self, start=0.0, end=1.0, step=1.0):
        super().__init__()
        self.start = start
        self.step = step
        self.end = end


class Output(ObjectWithTemplate):
    template = 'parameter/output/output'
    output_type = None

    def __init__(self, file_name):
        self.file_name = file_name


class Ascii(Output):
    template = 'parameter/output/ascii'
    output_type = 'ascii'

    def __init__(self, file_name, hit=0, singles=0, coincidences=0):
        super().__init__(file_name)
        self.hit = hit
        self.coincidences = coincidences
        self.singles = singles


class Binary(Output):
    template = 'parameter/output/binary'
    output_type = 'binary'

    def __init__(self, file_name, hit=0, singles=0, coincidences=0):
        super().__init__(file_name)
        self.hit = hit
        self.coincidences = coincidences
        self.singles = singles


class Root(Output):
    template = 'parameter/output/root'
    output_type = 'root'

    def __init__(self, file_name,
                 hit=None, singles=None, coincidences=None, optical=None, delay=None):
        super().__init__(file_name)
        self.hit = hit
        self.singles = singles
        self.coincidences = coincidences
        self.optical = optical
        self.delay = delay


class Sinogram(Output):
    template = 'parameter/output/sinogram'
    output_type = 'sinogram'

    def __init__(self, file_name,
                 input_,
                 radial_bin=None,
                 is_true_only=None,
                 is_raw_output=None,
                 tang_blurring=None,
                 axial_blurring=None,
                 is_store_delay=None,
                 is_store_scatter=None):
        super().__init__(file_name)
        self.input_ = input_
        self.radial_bin = radial_bin
        self.is_true_only = is_true_only
        self.is_raw_output = is_raw_output
        self.tang_blurring = tang_blurring
        self.axial_blurring = axial_blurring
        self.is_store_delay = is_store_delay
        self.is_store_scatter = is_store_scatter


class RandomEngine(ObjectWithTemplate):
    template = 'parameter/random_engine/random_engine'
    engine_type = 'JamesRandom'

    def __init__(self, seed='default'):
        self.seed = seed


class RandomEngineRanlux64(RandomEngine):
    engine_type = 'Ranlux64'


class RandomEngineJamesRandom(RandomEngine):
    engine_type = 'JamesRandom'


class RandomEngineMersenneTwister(RandomEngine):
    engine_type = 'MersenneTwister'


class Parameter(ObjectWithTemplate):
    template = 'parameter/parameter'

    def __init__(self, random_engine, outputs: List[Output], acquisition):
        self.acquisition = acquisition
        self.outputs = outputs
        self.random_engine = random_engine
