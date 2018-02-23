"""
make macs

Useage:
    write_macs(fs, experiment: Experiment)
"""
from fs.osfs import OSFS


def make_macs(experiment):
    from ..configs import configs
    from jinja2 import Environment, FileSystemLoader
    from pathlib import Path
    from .exp_args import get_experiment_with_mac
    experiment = get_experiment_with_mac(experiment)
    tpl_path = Path(configs['TEMPLATES_PATH']) / 'macs' / experiment.category
    env = Environment(loader=FileSystemLoader(str(tpl_path)))
    results = {}
    for n in experiment.mac_names():
        results[n] = (env.get_template('{}.mac'.format(n))
                      .render(**experiment.mac_configs(n)))
    return results


def write_macs(fs: OSFS, experiment):
    macs = make_macs(experiment)
    for n in macs:
        with fs.open('{}.mac'.format(n), 'w') as fout:
            print(macs[n], file=fout)
