import toolz, functools

isTuple = lambda e: isinstance(e, tuple)
isList = lambda e: isinstance(e, list)
isDict = lambda e: isinstance(e, dict)
isContainer = lambda e: any([isTuple(e), isList(e), isDict(e)])

def comp(*args):
    '''Function composition, where the functions are applied sequentially
        comp(f, g, h)(*args, **kwargs) == h(g(f(*args, **kwargs)))

       There are some subtle twists to handle multi arity functions. If an
        argument is of type list, it is treated as
            comp(
                lambda s: s.lower()
                [f, arg1, arg2, ..., argN]
            )

        where f(arg1, arg2, ..., argN, prev) 
        is executed with `prev` being the results of `lambda s: s.lower()`

        The same behavior can be achieved with a dict
            comp(
                lambda s: s.lower()
                {func=f, kwarg1=val1, kwarg2=val2, ..., kwargN=valN}
            )
        where f(prev, kwarg1=val1, kwarg2=val2, ..., kwargN=valN)
    '''
    def f(data):
        return reduce(
            lambda mem, ifunc: ifunc(mem),
            map(_apply_partial_if_list_or_dict, args),
            data
        )
    return f

def _apply_partial_if_list_or_dict(args):
    if isList(args):
        return functools.partial(*args)
    elif isDict(args):
        kwargs = dict(**args)
        func = kwargs.pop('func')
        return functools.partial(func, **kwargs)
    else:
        return args

@toolz.curry
def obj_path(path, entry):
    '''simple function to traverse a dict/json. 
    If path is not found, it returns None
    example:
        >>> obj_path('some.thing.0', {'some': {'thing': ['deep']}})
        'deep'
    '''
    paths = path.split('.', 1)
    i = paths.pop(0)
    if isList(entry) or isTuple(entry):
        ii = int(i)
        if ii < len(entry):
            val = entry[ii]
        else:
            return None
    elif isDict(entry):
        val = entry.get(i)
    else:
        return None
    if paths:
        return obj_path(paths[0], val)
    else:
        return val
