from .base import ObjectWithTemplate


class Verbose(ObjectWithTemplate):
    template = 'verbose'

    def __init__(self,
                 physics=0, cuts=0,
                 sd=0,
                 actions=0, actor=0, step=0,
                 error=0, warning=0,
                 output=0,
                 beam=0,
                 volume=0, image=0, geometry=0, core=0,
                 run=0, event=0, tracking=0):
        self.physics = physics
        self.cuts = cuts
        self.sd = sd
        self.actions = actions
        self.actor = actor
        self.step = step
        self.error = error
        self.warning = warning
        self.output = output
        self.beam = beam
        self.volume = volume
        self.image = image
        self.geometry = geometry
        self.core = core
        self.run = run
        self.event = event
        self.tracking = tracking


class MaterialDatabase(ObjectWithTemplate):
    template = 'misc/database'

    def __init__(self, path: str=None):
        self.path = path


class MaterialDatabaseLocal(MaterialDatabase):
    def __init__(self):
        super().__init__('./GateMaterials.db')

# TODO: add MaterialDatabaseShared


class Visualisation(ObjectWithTemplate):
    template = 'misc/visualisation'

    def __init__(self, is_disable=True):
        self.is_disable = is_disable
