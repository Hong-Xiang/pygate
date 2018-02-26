# class Environments:
#     def __init__(self):
#         self._envs = dict()

#     def get_or_create_env(self, experiment_set=None):
#         if experiment_set is None:
#             experiment_set = '_default'
#         if not experiment_set in self._envs:
#             self.create_environment(experiment_set)
#         return self._envs[experiment_set]

#     def create_environment(self, experiment_set):
#         from jinja2 import Environment, PackageLoader, ChoiceLoader
#         pkg_loaders = []
#         if experiment_set != '_default':
#             package = 'pygate.mac_files.{}'.format(experiment_set)
#             pkg_loaders.append(PackageLoader(package))
#         pkg_loaders.append(PackageLoader('pygate.components'))
#         env = Environment(loader=ChoiceLoader(pkg_loaders),
#                           line_statement_prefix='#!')
#         self._envs[experiment_set] = env


# envs = Environments()


# class ObjectWithTemplate:
#     template = None

#     def render(self):
#         return render_object(self)


# def render_object(obj: ObjectWithTemplate, experiment_set=None):
#     template_name = obj.template
#     if not template_name.endswith('.j2'):
#         template_name += '.j2'
#     template = (envs.get_or_create_env(experiment_set)
#                 .get_template(template_name))
#     return template.render(o=obj)

from . import __name__ as pkg_name
from ..utils.object_with_template import EnvironmentOfPackage, ObjectWithTemplateBase

env = EnvironmentOfPackage(pkg_name)


class ObjectWithTemplate(ObjectWithTemplateBase):
    pkg_env = env
