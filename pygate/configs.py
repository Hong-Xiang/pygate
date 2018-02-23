from pathlib import Path

def get_template_path():
    from pathlib import Path
    from . import templates
    return str(Path(templates.__file__).parent.absolute())

configs = {
    'TEMPLATES_PATH': get_template_path()
}