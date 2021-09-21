'Operating on functions'

import functools
import inspect
import toolz

empty = inspect._empty


def rcomp(*funcs):
    'reverse composition of functions'
    return toolz.comp(*reversed(funcs))

@toolz.curry
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
    '''The functtools.partial function as a decorator, it works very much like the 
        @curry decorator, except it always returns a function which will
        execute the next time it is called (regardless if there are missing
        arguments)
    '''
    @functools.wraps(func)
    def f(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    return f
