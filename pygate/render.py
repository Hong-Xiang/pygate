def get_environment(experiment_set):
    from jinja2 import Environment, PackageLoader, ChoiceLoader
    pkg_loaders = [PackageLoader('pygate.components'), ]
    if experiment_set is not None:
        package = 'pygate.mac_files.{}'.format(experiment_set)
        pkg_loaders.append(PackageLoader(package))
    env = Environment(loader=ChoiceLoader(pkg_loaders))

def get_template_finder(obj):
    from .components import renders as renders_c
    # if type(ob)


def render_object(obj, experiment_set=None):
    """
    """
    template = get_environment(experiment_set).get_template(obj.template)
    return template.render(**obj.render_kwarg_func(obj))
