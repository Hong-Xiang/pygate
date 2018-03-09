class KEYS:
    SUBMIT = 'submit'
    DRYRUN = 'dryrun'
    SUB_PREFIX = 'sub_prefix'
    SUB_PATTERNS = 'sub_patterns'
    SUB_FORMAT = 'sub_format'
    CLEAN = 'clean'
    ANALYSIS = 'analysis'
    INIT = 'init'


class SUBMIT_KEYS:
    BROADCAST = 'broadcast'
    SINGLE = 'single'


class CLEAN_KEYS:
    IS_SUBDIRECTORIES = 'is_subdirectories'
    ROOT_FILES = 'root_files'
    IS_SLURM_OUTPUTS = 'is_slurm_outputs'


class ANALYSIS_KEYS:
    SOURCE = 'source'
    TARGET = 'target'
    ANALYSIS_TYPE = 'analysis_type'


class INIT_KEYS:

    EXTERNAL = 'external'

    class EXTERNAL_KEYS:
        SOURCE = 'source'
        TARGET = 'target'

    MAC = 'mac'

    class MAC_KEYS:
        SIMULATION_CONF = 'simulation_conf'

    SHELL = 'shell'

    class SHELL_KEYS:
        pass

    PHANTOM = 'phantom'

    class PHANTOM_KEYS:
        pass


init_config = {
    INIT_KEYS.EXTERNAL: [
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/GateMaterials.db'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Materials.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Surfaces.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/HitsConverter.C'},
    ],
    INIT_KEYS.SHELL: {

    }
}


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
    },
    KEYS.INIT: init_config



}
