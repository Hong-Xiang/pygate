class EnvironmentOfPackage:
    def __init__(self, pkg_name):
        self._env = None
        self.name = pkg_name

    def get_or_create_env(self):
        from jinja2 import Environment, PackageLoader
        if self._env is None:
            self._env = Environment(loader=PackageLoader(self.name))
            self._env.filters['default_suffix'] = default_suffix
            self._env.filters['ds'] = default_suffix
        return self._env


"""
Custom filters
"""


def default_suffix(s: str, suffix: str, is_auto_add_point_prefix=True):
    if is_auto_add_point_prefix and not suffix.startswith('.'):
        suffix = '.' + suffix
    if not s.endswith(suffix):
        s += suffix
    return s


class ObjectWithTemplateBase:
    pkg_env = None
    template = None

    def template_name(self):
        template_name = self.template
        if not template_name.endswith('.j2'):
            template_name += '.j2'
        return template_name

    def render(self):
        template = (self.pkg_env.get_or_create_env()
                    .get_template(self.template_name()))
        return template.render(o=self)
