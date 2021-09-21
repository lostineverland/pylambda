'tools to handle lazy objects (sequences)'

def take(n, seq):
    vals = []
    for i in range(n):
        try:
            vals += [next(seq)]
        except StopIteration:
            return vals
    return vals

def limit_seq(seq, limit):
    '''allows you to set a hard limit on a sequence
    '''
    for i, val in enumerate(seq):
        if i == limit: break
        yield val
