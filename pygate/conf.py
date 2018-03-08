class KEYS:
    SUBMIT = 'submit'
    DRYRUN = 'dryrun'
    SUB_PREFIX = 'sub_prefix'
    SUB_PATTERNS = 'sub_patterns'
    SUB_FORMAT = 'sub_format'


class SUBMIT_KEYS:
    BROADCAST = 'broadcast'
    SINGLE = 'single'


config = {
    KEYS.SUBMIT: {
        SUBMIT_KEYS.BROADCAST: ['run.sh'],
        SUBMIT_KEYS.SINGLE: ['post.sh'],
    },
    KEYS.DRYRUN: False,
    KEYS.SUB_PREFIX: 'sub'
}
