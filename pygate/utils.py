def get_scripts_path():
    import pygate
    from dxpy.filesystem import Path
    p = Path(pygate.__file__)
    return Path(p.father) / 'scripts'


def load_script(name):
    script_file = (get_scripts_path() / name).abs
    with open(script_file) as fin:
        return fin.read()


def sub_dir_filters(config):
    return ['{name}*'.format(name=config['split']['name'])]
