from . import __name__ as pkg_name
from ..utils.object_with_template import EnvironmentOfPackage, ObjectWithTemplateBase

env = EnvironmentOfPackage(pkg_name)


class ObjectWithTemplate(ObjectWithTemplateBase):
    pkg_env = env


