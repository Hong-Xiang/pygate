class _BoxWithSurface:
    def __init__(self, hx, hy, hz, surfaces: dict, material=None):
        self.hx = hx
        self.hy = hy
        self.hz = hz
        self.surfaces = surfaces
        self.material = material


def render_geometry(world: _BoxWithSurface,
                    optical_system, crystal, silicon_multiplier):
    """
    """
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader(__name__))
    template = env.get_template('geometry.mac')
    return template.render(world=world,
                           optical_system=optical_system,
                           crystal=crystal,
                           silicon_multiplier=silicon_multiplier)
