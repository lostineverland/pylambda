'Operating on functions'

import functools
import inspect
import toolz

empty = inspect._empty


def _func_args(func):
    '''inspect a function to understand which arguments are known and 
        which are missing
    '''
    required = []
    known = {}
    args = iter(inspect.signature(func).parameters.items())
    for key, val in args:
        if str(val).startswith('*'):
            required += [str(val)]
        else:
            required += [key]
        known[key] = val.default
    # print('required: {}\nknown: {}'.format(required, known))
    return required, known

def _check_missing(args, kwargs, required, known):
    '''The curry function sets up a list and a dict to keep track
        of the function values and which ones are missing. This method
        takes the new values, and compares it to what is known to return
        the new state of known and missing
    '''
    # print('args: {}\nkwargs: {}\nrequired: {}\nknown: {}'.format(args, kwargs, required, known))
    # kwargs are purposeful, thus populate known values with kwargs first
    known = toolz.merge(known, kwargs)
    # clear the new kwargs from required
    not_in_kwargs = lambda k: k not in kwargs
    required = list(filter(not_in_kwargs, required))
    # populate known with the values from args
    for i, val in enumerate(args):
        if len(required) > i:
            # here we handle *args
            if required[i].startswith('*'):
                known[required[i][1:]] = args[i:]
                break
            else:
                known[required[i]] = val
    is_empty = lambda k: known[k.replace('*', '')] is empty
    missing = list(filter(is_empty, required))
    required = required[i+1:] if args else required
    # print('missing: {}\nrequired: {}\nknown: {}'.format(missing, required, known))
    return missing, required, known

def curry(*f_args, **kwargs):
    '''Your typical currying decorator, but this one lets you feed it knowledge
        of the arguments expected. This is useful if you're stacking decorators.

        Limitations: 
            1. The curried functions may not use *args, the args must be called out.
            2. The target function will eventually be called with keyword
            arguments, thus if the target function prevents the use of keywords (
            throug the use of '/' e.g def(a, b, /, c)... ) it will fail execution
            with a 'TypeError'
    '''
    func = f_args[0]
    args = f_args[1:]
    if not callable(func):
        return lambda f: curry(f, *f_args, **kwargs)
    if args:
        required = args
        known = toolz.merge(dict(zip(args, [empty] * len(args))), kwargs)
    else:
        required, known = _func_args(func)
    @functools.wraps(func)
    def funcy(*a, **kw):
        missing, args, kwargs = _check_missing(a, kw, required, known)
        if missing:
            return curry(func, *args, **kwargs)
        else:
            return func(**kwargs)
    return funcy

def rcomp(*funcs):
    'reverse composition of functions'
    return toolz.comp(*reversed(funcs))

@curry
def field_filter(fields, entry):
    'filter for the specified fields from the entry'
    missing = object()
    not_missing = lambda i: i != missing
    return toolz.valfilter(
        not_missing,
        dict(zip(fields, toolz.get(fields, entry, default=missing)))
    )


def field_filter_in(fields, entry):
    '''filter for the specified nested fields from the entry
        nesting is dot delimited: 
        field_filter_in(
            ['some.nested.key'], 
            {'some':{'nested':{'key': 'value'}}}) == {'some.nested.key': 'value'}
        to rename the key, the entry in fields should be a dict:
        field_filter_in(
            ['some.nested.key', {'some.nested.key': 'better_name'}], 
            {'some':{'nested':{'key': 'value'}}}) == {'some.nested.key': 'value', 'better_name': 'value'}
            
    '''
    missing = object()
    not_missing = lambda i: i != missing
    nested_get = rcomp(
        lambda i: i if isinstance(i, str) else next(iter(i.keys())),
        lambda s: s.split('.'),
        lambda key: toolz.get_in(key, entry, default=missing)
    )
    # last_field_arg = rcomp(
    #     lambda s: s.split('.'),
    #     tlz.get(-1)
    # )
    get_key = lambda i: i if isinstance(i, str) else next(iter(i.values()))
    entry_ = {get_key(field): nested_get(field) for field in fields}
    return toolz.valfilter(
        not_missing,
        entry_
    )

def partial(func):
    '''The partial function as a decorator, it works very much like the 
        @curry decorator, except it always returns a function which will
        execute the next time it is called (regardless if there are missing
        arguments)
    '''
    @functools.wraps(func)
    def f(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    return f
