def ignore_empty_newlines(s):
    return '\n'.join([x for x in s.split('\n') if x != ''])

def join_multiple(s, to_join):
    return to_join.join([x for x in s.split(to_join) if x != '']) 
