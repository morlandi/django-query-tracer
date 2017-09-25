# NOTE: currently unused

import pprint

try:
    import sqlparse
except ImportError:
    class sqlparse:
        @staticmethod
        def format(text, *args, **kwargs):
            return text


def trace(message, prettify=False):
    if type(message) is list:
        text = ' '.join([str(item) for item in message])
    else:
        text = str(message)
    if prettify:
        text = pprint.pformat(text)
    print '\x1b[1;33;40m' + text + '\x1b[0m'


def prettyprint_queryset(qs, colorize=True):
    if colorize: print '\x1b[1;33;40m'
    print sqlparse.format(str(qs.query), reindent=True, keyword_case='upper')
    if colorize: print '\x1b[0m'


def trace_func(fn):
    def func_wrapper(*args, **kwargs):
        trace('>>> %s()' % fn.func_name)
        trace('    args: %s' % str(args))
        trace('    kwargs: %s' % str(kwargs))
        ret = fn(*args, **kwargs)
        trace('<<< %s()' % fn.func_name)
        return ret
    return func_wrapper
