class KEYS:
    SUBMIT = 'submit'
    DRYRUN = 'dryrun'
    SUB_PREFIX = 'sub_prefix'
    SUB_PATTERNS = 'sub_patterns'
    SUB_FORMAT = 'sub_format'
    CLEAN = 'clean'
    ANALYSIS = 'analysis'
    INIT = 'init'
    NB_SPLIT = 'nb_split'


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
    NAME = 'name'
    OUTPUT = 'output'
    ANALYSIS_TYPE = 'subcommand'


class INIT_KEYS:

    BROADCAST = 'broadcast'

    class BROADCAST_KEYS:
        TARGETS = 'targets'
        NO_EXT = 'no_ext'

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
        PYGATE_ANALYSIS = 'pygate_analysis'
        PARTITION = 'partition'

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
    INIT_KEYS.SHELL_KEYS.PARTITION: 'cpu',
}

shell_post_run_config = {
    INIT_KEYS.SHELL_KEYS.GATE_VERSION: '8.0',
    INIT_KEYS.SHELL_KEYS.TASK: [
        {INIT_KEYS.SHELL_KEYS.TASK_NAME:  INIT_KEYS.SHELL_KEYS.MERGE,
         INIT_KEYS.SHELL_KEYS.TARGET: 'result.root',
         INIT_KEYS.SHELL_KEYS.METHOD: 'hadd'},
        {INIT_KEYS.SHELL_KEYS.TASK_NAME: INIT_KEYS.SHELL_KEYS.ROOT_ANALYSIS,
         INIT_KEYS.SHELL_KEYS.TARGET: 'result.root',
         INIT_KEYS.SHELL_KEYS.ROOT_C_FILE: 'Hits2CSV.C'},
        {INIT_KEYS.SHELL_KEYS.TASK_NAME: INIT_KEYS.SHELL_KEYS.PYGATE_ANALYSIS,
         ANALYSIS_KEYS.SOURCE: 'optical.csv',
         ANALYSIS_KEYS.TARGET: 'optical.h5',
         ANALYSIS_KEYS.ANALYSIS_TYPE: 'gamma_edep'}
    ],
    INIT_KEYS.SHELL_KEYS.TARGET: 'post.sh',
    INIT_KEYS.SHELL_KEYS.SHELL_TYPE: 'bash',
    INIT_KEYS.SHELL_KEYS.PARTITION: 'cpu',
}

init_config = {
    INIT_KEYS.EXTERNAL: [
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/GateMaterials.db'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Materials.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Surfaces.xml'},
        {INIT_KEYS.EXTERNAL_KEYS.SOURCE: '/mnt/gluster_NoGPU/share/pygate/Hits2CSV.C'},
    ],
    INIT_KEYS.SHELL: {
        INIT_KEYS.SHELL_KEYS.RUN: shell_run_config,
        INIT_KEYS.SHELL_KEYS.POST_RUN: shell_post_run_config,
    },
    INIT_KEYS.BROADCAST: {
        INIT_KEYS.BROADCAST_KEYS.TARGETS: ['main.mac'],
        INIT_KEYS.BROADCAST_KEYS.NO_EXT: False,
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
        CLEAN_KEYS.ROOT_FILES: [],
    },
    KEYS.INIT: init_config,
    KEYS.NB_SPLIT: 10,
    KEYS.ANALYSIS: {
        ANALYSIS_KEYS.SOURCE: 'result.csv',
        ANALYSIS_KEYS.TARGET: 'result.h5',
        ANALYSIS_KEYS.ANALYSIS_TYPE: 'gamma_edep'
    }



}
