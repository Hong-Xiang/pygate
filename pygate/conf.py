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
        SIMULATION_DEMO = 'simulation_demo'

    SHELL = 'shell'

    class SHELL_KEYS:
        RUN = 'run'
        POST_RUN = 'post_run'
        TASK = 'task'
        TASK_NAME = 'task_name'
        TARGET = 'target'
        GATE_SIMULATION = 'gate_simulation'
        ROOT_ANALYSIS = 'root_analysis'
        ROOT_C_FILE = 'root_c_file'
        MERGE = 'merge'
        SOURCE = 'source'
        METHOD = 'method'
        GATE_VERSION = 'gate_version'
        SHELL_TYPE = 'shell_type'

    PHANTOM = 'phantom'

    class PHANTOM_KEYS:
        pass


shell_run_config = {
    INIT_KEYS.SHELL_KEYS.GATE_VERSION: '8.0',
    INIT_KEYS.SHELL_KEYS.SHELL_TYPE: 'bash',
    INIT_KEYS.SHELL_KEYS.TASK: [
        {INIT_KEYS.SHELL_KEYS.TASK_NAME: INIT_KEYS.SHELL_KEYS.GATE_SIMULATION,
         INIT_KEYS.SHELL_KEYS.TARGET: 'main.mac'},
    ],
    INIT_KEYS.SHELL_KEYS.TARGET: 'run.sh',
}

shell_post_run_config = {
    INIT_KEYS.SHELL_KEYS.TASK: [
        {INIT_KEYS.SHELL_KEYS.TASK_NAME:  INIT_KEYS.SHELL_KEYS.MERGE,
         INIT_KEYS.SHELL_KEYS.TARGET: 'result.root',
         INIT_KEYS.SHELL_KEYS.METHOD: 'hadd'},
        {INIT_KEYS.SHELL_KEYS.TASK_NAME: INIT_KEYS.SHELL_KEYS.ROOT_ANALYSIS,
         INIT_KEYS.SHELL_KEYS.TARGET: 'result.root',
         INIT_KEYS.SHELL_KEYS.ROOT_C_FILE: 'HitsConverter.C'}
        # {INIT_KEYS.SHELL_KEYS.ROOT_ANALYSIS: }
    ],
    INIT_KEYS.SHELL_KEYS.TARGET: 'post.sh',
    INIT_KEYS.SHELL_KEYS.SHELL_TYPE: 'bash'
}

init_config = {
    INIT_KEYS.EXTERNAL: [
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/GateMaterials.db'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Materials.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Surfaces.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/HitsConverter.C'},
    ],
    INIT_KEYS.SHELL: {
        INIT_KEYS.SHELL_KEYS.RUN: shell_run_config,
        INIT_KEYS.SHELL_KEYS.POST_RUN: shell_post_run_config,
    },
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