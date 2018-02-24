def ignore_empty_newlines(s):
    return '\n'.join([x for x in s.split('\n') if x != ''])
