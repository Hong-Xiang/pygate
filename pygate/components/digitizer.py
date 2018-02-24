from .base import ObjectWithTemplate


class Insertable(ObjectWithTemplate):
    template = 'digitizer/insertable'
    insertable_type = None

    def __init__(self, name=None, define_name=False, no_explicit_insert=False):
        self.name = name
        self.base = None
        self.define_name = define_name
        self.no_explict_insert = no_explicit_insert


class Singles(Insertable):
    template = 'digitizer/singles/singles'

    def __init__(self, plugins=None, name='Singles', define_name=False, no_explicit_insert=False):
        super().__init__(name, define_name, no_explicit_insert=True)
        self.plugins = plugins
        for p in self.plugins:
            p.base = self


class Adder(Insertable):
    insertable_type = 'adder'

    def __init__(self, name='adder', define_name=False):
        super().__init__(name, define_name)


class Readout(Insertable):
    template = 'digitizer/singles/readout'
    insertable_type = 'readout'

    def __init__(self, policy='TakeEnergyCentroid', depth=1,
                 name='readout', define_name=False):
        super().__init__(name, define_name)
        self.policy = policy
        self.depth = depth


class Blurring(Insertable):
    template = 'digitizer/singles/blurring'
    insertable_type = 'blurring'

    def __init__(self, law=None, resolution=0.15, eor=511, slope=None,
                 name='blurring', define_name=False):
        self.law = law
        self.resolution = resolution
        self.eor = eor
        self.slope = slope


class CrystalBlurring(Blurring):
    insertable_type = 'crystalBlurring'

    def __init__(self, res_window, qe, eor, name, define_name):
        super().__init__(name=name, define_name=define_name)


class SpBlurring(Blurring):
    insertable_type = 'spBlurring'
    pass


class Holder(Insertable):
    template = 'digitizer/singles/holder'
    holder_name = None
    insertable_type = None

    def __init__(self, value, name=None, define_name=False):
        super().__init__(name, define_name)


class ThresHolder(Holder):
    holder_name = 'Threshold'
    insertable_type = 'thresholder'


class UpHolder(Holder):
    holder_name = 'Uphold'
    insertable_type = 'upholder'


class TimeResolution(Insertable):
    template = 'digitizer/singles/time_resolution'
    insertable_type = 'timeResolution'

    def __init__(self, resolution, name=None, define_name=False):
        super().__init__(name, define_name)
        self.resolution = resolution


class WithBuffer(Insertable):
    template = 'digitizer/singles/buffer'

    def __init__(self, size=None, mode=None, name=None, define_name=False):
        super().__init__(name, define_name)
        self.size = size
        self.mode = mode


class MemoryBuffer(WithBuffer):
    template = 'digitizer/singles/memory_buffer'
    insertable_type = 'buffer'

    def __init__(self, read_freq=None, size=None, mode=None, name=None, define_name=False):
        super().__init__(name, size, mode, name, define_name)
        self.read_freq = read_freq


class DeadTime(WithBuffer):
    template = 'digitizer/singles/dead_time'
    insertable_type = 'deadtime'

    def __init__(self, volume, t, mode, buffer_size, buffer_mode):
        super().__init__(buffer_size, buffer_mode, name, define_name)
        self.volume = volume
        self.t = t
        self.mode = mode


class SinglesChain(Insertable):
    def __init__(self, name, define_name=True):
        super().__init__(name, define_name)


class CoincidenceSorter(Insertable):
    def __init__(self, input_=None, window=None, offset=None, name='Coincidences', define_name=False):
        super().__init__(name, define_name)


class CoincidencesChain(Insertable):
    def __init__(self, inputs, name, use_priority=True, define_name=True):
        super().__init__(name, define_name)
        self.inputs = inputs
        self.use_priority = use_priority
