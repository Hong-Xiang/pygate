from .base import ObjectWithTemplate


class Acquisition(ObjectWithTemplate):
    template = 'parameter/acquisition/acquisition'
    acquisition_type = None


class Primaries(Acquisition):
    template = 'parameter/acquisition/primaries'
    acquisition_type = 'primaries'

    def __init__(self, number=10000):
        super().__init__()
        self.number = number


class Period(Acquisition):
    template = 'parameter/acquisition/period'
    acquisition_type = 'period'

    def __init__(self, start=0.0, end=1.0, step=1.0):
        super().__init__()
        self.start = start
        self.slice = step
        self.end = end


class Output(ObjectWithTemplate):
    template = 'parameter/output/output'
    output_type = None

    def __init__(self, file_name):
        self.file_name = file_name


class Ascii(Output):
    template = 'parameter/output/ascii'
    output_type = 'ascii'

    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0):
        super().__init__(file_name)
        self.hit_flag = hit_flag
        self.coincidence_flag = coincidence_flag
        self.single_flag = single_flag


class Binary(Output):
    template = 'parameter/output/binary'

    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0):
        super().__init__(file_name)
        self.hit_flag = hit_flag
        self.coincidence_flag = coincidence_flag
        self.single_flag = single_flag


class Root(Output):
    template = 'parameter/output/root'

    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0, optical_flag=0):
        super().__init__(file_name)
        self.hit_flag = hit_flag
        self.single_flag = single_flag
        self.coincidence_flag = coincidence_flag
        self.optical_flag = optical_flag


class Sinogram(Output):
    template = 'parameter/output/sinogram'

    def __init__(self, file_name, input_name, radial_bin=None, true_only_flag=None, raw_out_flag=None,
                 tang_blur=None, axial_blur=None, delay_flag=None, scatter_flag=None):
        super().__init__(file_name)
        self.input_name = input_name
        self.radial_bin = radial_bin
        self.true_only_flag = true_only_flag
        self.raw_out_flag = raw_out_flag
        self.tang_blur = tang_blur
        self.axial_blur = axial_blur
        self.delay_flag = delay_flag
        self.scatter_flag = scatter_flag


class RandomEngine(ObjectWithTemplate):
    template = 'parameter/random_engine/random_engine'
    engine_type = 'JameRandom'

    def __init__(self, seed='default'):
        self.seed = seed


class RandomEngineRanlux64(RandomEngine):
    engine_type = 'Ranlux64'


class RandomEngineJameRandom(RandomEngine):
    engine_type = 'JameRandom'


class RandomEngineMersenneTwister(RandomEngine):
    engine_type = 'MersenneTwister'


class Parameter(ObjectWithTemplate):
    template = 'parameter/parameter'
    def __init__(self, acquisition=None, output=None, random_engine=None):
        self.acquisition = acquisition
        self.output = output
        self.random_engine = random_engine
