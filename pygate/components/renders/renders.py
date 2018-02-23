from ..geometry import Vec3, Volume, Box
SUPPORTED_TYPES = (Vec3, Volume, Box)
TEMPLATE_MAP = {
    Vec3: 'vec3',
    Volume: 'volume',
    Box: 'box'
}
KWARGS_MAP = {
    Vec3: lambda o: {'v': o},
    Volume: lambda o: {'v': o}
    Box: lambda o: {'v': o}
}


def check_support(o):
    if not type(o) in SUPPORTED_TYPES:
        raise "No template support for type {}.".format(type(o))


def get_render_kwargs(o):
    check_support(o)
    return KWARGS_MAP[type(o)]


def get_template(o):
    check_support(o)
    return TEMPLATE_MAP(type(o))
