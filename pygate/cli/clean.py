import click

from ..conf import config, KEYS, CLEAN_KEYS
from .main import pygate
from typing import Iterable


def clean_kernel(is_subdirectories, subdirectory_patterns: Iterable[str],
                 root_file_patterns: Iterable[str],
                 is_slurm_outputs, dryrun: bool):
    from pygate.routine import cleaner
    d = cleaner.Directory('.')
    ops = []
    if is_subdirectories:
        ops.append(cleaner.OpCleanSubdirectories(subdirectory_patterns))
    if len(root_file_patterns) > 0:
        ops.append(cleaner.OpCleanSource(root_file_patterns))
    if is_slurm_outputs:
        ops.append(cleaner.OpCleanFilesInAllDirectories(['*.out', '*.err'],
                                                        subdirectory_patterns))
    r = cleaner.RoutineOnDirectory(d, ops, dryrun)
    r.work()
    return r.echo()


@pygate.command()
@click.option('--subdirectories', '-d', help='remove subdirectories', is_flag=True)
@click.option('--root-files', '-f', help='remove files in work directory', multiple=True)
@click.option('--slurm-outputs', '-s', help='remove *.out *.err files', is_flag=True)
def clean(subdirectories, root_files, slurm_outputs):
    clean_conf = config.get(KEYS.CLEAN, {})
    if subdirectories is None:
        subdirectories = clean_conf[CLEAN_KEYS.IS_SUBDIRECTORIES]
    if slurm_outputs is None:
        slurm_outputs = clean_conf[CLEAN_KEYS.IS_SLURM_OUTPUTS]
    config_root_files = clean_conf[CLEAN_KEYS.ROOT_FILES]
    if len(config_root_files) > 0:
        root_files = tuple(list(root_files) + list(config_root_files))
    click.echo(clean_kernel(subdirectories, config.get(KEYS.SUB_PATTERNS),
                            root_files, slurm_outputs,
                            config.get(KEYS.DRYRUN)))
