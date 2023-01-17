'tools to handle lazy objects (sequences)'

def take(n, seq):
    vals = []
    for i in range(n):
        try:
            vals += [next(seq)]
        except StopIteration:
            return vals
    return vals

def limit_seq(limit, seq):
    '''allows you to set a hard limit on a sequence
    '''
    for i, val in enumerate(seq):
        if i == limit: break
        yield val

def loop(val):
    if isinstance(val, list):
        while True:
            for i in val:
                yield i
    while True:
        yield val

def nth(n, seq):
    for i in range(n):
        try:
            val = next(seq)
        except StopIteration:
            return val
    return val

def last(seq):
    for i in seq:
        val = i
    return val

