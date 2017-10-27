from fs.osfs import OSFS
from .template.service import MacMaker
from .utils import load_script
from .config import config as c


class ConfigMaker:
    @classmethod
    def _make_pygate_config(cls, fs, target, config_filename=None):
        config_filename = config_filename or c['pygate_config']
        with fs.opendir(target) as d:
            with d.open(config_filename, 'w') as fout:
                print(load_script(config_filename), file=fout)

    @classmethod
    def _make_mac_config(cls, fs, target, config_filename: str=None):
        if config_filename.endswith('.yml'):
            config_filename = config_filename[:-4]
        MacMaker.make_yml(config_filename)

    @classmethod
    def make(cls, fs, target, pygate_config=None, mac_config=None):
        pygate_config = pygate_config or c['pygate_config']
        mac_config = mac_config or c['mac_config']
        cls._make_pygate_config(fs, target, pygate_config)
        cls._make_mac_config(fs, target, mac_config)
