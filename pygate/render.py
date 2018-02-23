def render_object(obj):
    """
    """
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader(__name__))
    template = env.get_template('geometry.mac')
    return template.render(world=world,
                           optical_system=optical_system,
                           crystal=crystal,
                           silicon_multiplier=silicon_multiplier)