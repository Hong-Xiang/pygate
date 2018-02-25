class Acquisition:
    def __init__(self, category):
        self.category = category


class Primaries(Acquisition):
    def __init__(self, number=10000):
        super(Primaries, self).__init__(category='primaries')
        self.number = number


class Period(Acquisition):
    def __init__(self, time_start=0.0, time_stop=1.0, time_slice=1.0):
        super(Period, self).__init__(category='peroid')
        self.time_start = time_start
        self.time_slice = time_slice
        self.time_stop = time_stop


class Output:
    def __init__(self, type, file_name):
        self.type = type
        self.file_name = file_name


class Ascii(Output):
    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0):
        super(Ascii, self).__init__(type='ascii', file_name=file_name)
        self.hit_flag = hit_flag
        self.coincidence_flag = coincidence_flag
        self.single_flag = single_flag


class Binary(Output):
    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0):
        super(Binary, self).__init__(type='binary', file_name=file_name)
        self.hit_flag = hit_flag
        self.coincidence_flag = coincidence_flag
        self.single_flag = single_flag


class Root(Output):
    def __init__(self, file_name, hit_flag=0, single_flag=0, coincidence_flag=0, optical_flag=0):
        super(Root, self).__init__(type='root', file_name=file_name)
        self.hit_flag = hit_flag
        self.single_flag = single_flag
        self.coincidence_flag = coincidence_flag
        self.optical_flag = optical_flag


class Sinogram(Output):
    def __init__(self, file_name, input_name, radial_bin=None, true_only_flag=None, raw_out_flag=None,
                 tang_blur=None, axial_blur=None, delay_flag=None, scatter_flag=None):
        super(Sinogram, self).__init__(type='sinogram', file_name=file_name)
        self.input_name = input_name
        self.radial_bin = radial_bin
        self.true_only_flag = true_only_flag
        self.raw_out_flag = raw_out_flag
        self.tang_blur = tang_blur
        self.axial_blur = axial_blur
        self.delay_flag = delay_flag
        self.scatter_flag = scatter_flag

class RandomEngine:
    engine_list = ['Ranlux64','JameRandom','MersenneTwister']
    def __init__(self, engine_name = 'JameRandom', seed = 'default'):
        self.engine_name = engine_name
        self.seed = seed


class Parameter:
    def __init__(self, acquisition=None, output=None, random_engine=None):
        self.acquisition = acquisition
        self.output = output
        self.random_engine = random_engine
