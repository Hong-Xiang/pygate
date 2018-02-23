class Environments:
    def __init__(self):
        self._envs = dict()

    def get_or_create_env(self, experiment_set=None):
        if experiment_set is None:
            experiment_set = '_default'
        if not experiment_set in self._envs:
            self.create_environment(experiment_set)
        return self._envs[experiment_set]

    def create_environment(self, experiment_set):
        from jinja2 import Environment, PackageLoader, ChoiceLoader
        pkg_loaders = [PackageLoader('pygate.components'), ]
        if experiment_set != '_default':
            package = 'pygate.mac_files.{}'.format(experiment_set)
            pkg_loaders.append(PackageLoader(package))
        env = Environment(loader=ChoiceLoader(pkg_loaders),
                          line_statement_prefix='#!')
        self._envs[experiment_set] = env


envs = Environments()


class ObjectWithTemplate:
    template = None

    def render(self):
        return render_object(self)


def render_object(obj: ObjectWithTemplate, experiment_set=None):
    template = (envs.get_or_create_env(experiment_set)
                .get_template(obj.template))
    return template.render(o=obj)
