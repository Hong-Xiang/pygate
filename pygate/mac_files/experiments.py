class ExperimentWithMacs:
    category = None

    def __init__(self, logic_experiment):
        self._e = logic_experiment

    def mac_names(self):
        return tuple()

    def mac_configs(self, name):
        return dict()


class ExperimentDevelop(ExperimentWithMacs):
    category = 'monolithic_crystal'

    def __init__(self, logic_experiment):
        super().__init__(logic_experiment)

    def mac_names(self):
        return ('geometry',)

    def mac_configs(self, name):
        class BoxWithSurface:
            def __init__(self, hx, hy, hz, surfaces):
                self.hx = hx
                self.hy = hy
                self.hz = hz
                self.surfaces = surfaces
        optical_system = BoxWithSurface(
            10.0, 10.0, 10.0, {'crystal1': 'surface1'})
        crystal = BoxWithSurface(10.0, 10.0, 10.0, {
                                 'optical_system': 'surface2.1', 'silicon_multiplier': 'surface2.2'})
        silicon_multiplier = BoxWithSurface(
            10.0, 10.0, 10.0, {'crystal': 'surface3'})
        return {'optical_system': optical_system,
                'crystal': crystal,
                'silicon_multiplier': silicon_multiplier, }


def get_experiment_with_mac(experiment) -> ExperimentWithMacs:
    return ExperimentDevelop(experiment)
