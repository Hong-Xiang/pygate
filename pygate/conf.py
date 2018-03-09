class KEYS:
    SUBMIT = 'submit'
    DRYRUN = 'dryrun'
    SUB_PREFIX = 'sub_prefix'
    SUB_PATTERNS = 'sub_patterns'
    SUB_FORMAT = 'sub_format'
    CLEAN = 'clean'


class SUBMIT_KEYS:
    BROADCAST = 'broadcast'
    SINGLE = 'single'


class CLEAN_KEYS:
    IS_SUBDIRECTORIES = 'is_subdirectories'
    ROOT_FILES = 'root_files'
    IS_SLURM_OUTPUTS = 'is_slurm_outputs'


config = {
    KEYS.SUBMIT: {
        SUBMIT_KEYS.BROADCAST: ['run.sh'],
        SUBMIT_KEYS.SINGLE: ['post.sh'],
    },
    KEYS.DRYRUN: False,
    KEYS.SUB_PREFIX: 'sub',
    KEYS.CLEAN: {
        CLEAN_KEYS.IS_SUBDIRECTORIES: True,
        CLEAN_KEYS.IS_SLURM_OUTPUTS: False,
        CLEAN_KEYS.ROOT_FILES: (),
    }
}
