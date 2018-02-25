def ignore_empty_newlines(s):
    return '\n'.join([x for x in s.split('\n') if x != ''])


def join_multiple(s, to_join):
    return to_join.join([x for x in s.split(to_join) if x != ''])


def ignore_multiple_whitespaces(s):
    return join_multiple(join_multiple(s, ' '), '\n')


def assert_equal_ignoring_multiple_whitespaces(obj, first, second):
    return obj.assertEqual(ignore_multiple_whitespaces(first),
                           ignore_multiple_whitespaces(second))
