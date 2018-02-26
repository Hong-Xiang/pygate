from typing import List


def ignore_empty_newlines(s):
    return '\n'.join([x for x in s.split('\n') if x != ''])


def join_multiple(s, to_join):
    return to_join.join([x for x in s.split(to_join) if x != ''])


def drop_comments(s, comment_prefix='#'):
    lines = s.split('\n')
    lines = [s for s in lines if not s.startswith(comment_prefix)]
    return '\n'.join(lines)


def rstrip(s):
    lines = s.split('\n')
    lines = [s.rstrip() for s in lines]
    return '\n'.join(lines)

def expand_tabs(s, number_of_spaces=4):
    return s.replace('\t', ' '*number_of_spaces)

def ignore_multiple_whitespaces(s: str):
    s = join_multiple(s, ' ')
    s = join_multiple(s, '\n')
    s = rstrip(s)
    s = drop_comments(s)
    return s


def assert_equal_ignoring_multiple_whitespaces(obj, first, second):
    return obj.assertEqual(ignore_multiple_whitespaces(first),
                           ignore_multiple_whitespaces(second))
