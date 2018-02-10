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

def applicative_func(*funcs):
    '''This function serves as an applicative functor, or a loose 
        interpretation of an applicative functor. In practice it works
        like map, with the functions and values inverted. It applies a
        list of functions to some arguments.
        Example:
            add = lambda x, y: x + y
            subtract = lambda x, y: x - y
            multiply = lambda x, y: x * y
            divide = lambda x, y: x / y
            power = lambda x, y: x ** y

            oper = applicative_func(add, subtract, multiply, divide, power)
            oper(8, 2)

            >>> [10, 6, 16, 4, 64]

        Much like the composition function, any value in the function list
        which either a list or a dict, will be treated as a function with 
        partial arguments
    '''
    def functor(*args):
        applicator = lambda f: f(*args)
        return map(applicator, _apply_partial_if_list_or_dict(funcs))
    return functor

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
