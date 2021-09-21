"""Some types to make dict objects easier to traverse in the repl
    This takes advantage of the repl behavior which triggers __getattribute__
    multiple times with string inputs such as "__dict__" or "__class__" when
    the Tab key is pressed.
"""

import readline


isTuple = lambda e: isinstance(e, tuple)
isList = lambda e: isinstance(e, list)
isDict = lambda e: isinstance(e, dict)
isContainer = lambda e: any([isTuple(e), isList(e), isDict(e)])

class otupl(tuple):
    def __getitem__(self, item):
        val = super(otupl, self).__getitem__(item)
        if isList(val):
            return olist(val)
        elif isDict(val):
            return odict(val)
        elif isTuple(val):
            return otupl(val)
        return val
    def __getattribute__(self, item):
        if item == '__dict__':
            print('\nlength:', len(self))
            print('\n{}'.format(readline.get_line_buffer()), end='')
        if item[0] == 'i' and item[1].isdigit():
            return super(otupl, self).__getitem__(int(item[1:]))
        else:
            return getattr(super(otupl, self), item)

class olist(list):
    def __getitem__(self, item):
        val = super(olist, self).__getitem__(item)
        if isList(val):
            return olist(val)
        elif isDict(val):
            return odict(val)
        elif isTuple(val):
            return otupl(val)
        return val
    def __getattribute__(self, item):
        if item == '__dict__':
            print('\nlength:', len(self))
            print('\n{}'.format(readline.get_line_buffer()), end='')
        if item[0] == 'i' and item[1].isdigit():
            return super(olist, self).__getattribute__('__getitem__')(int(item[1:]))
        else:
            return getattr(super(olist, self), item)

class odict(dict):
    def __init__(self, entry):
        # self.mem = ''
        super(odict, self).__init__(entry)

    def __getattribute__(self, item):
        if item == '__dict__':
            # if super(odict, self).__getattribute__('mem') == '__dict__':
            #     print('stuff is here')
            # else:
            #     print('\nitem: {}\n'.format(super(odict, self).keys()), end='')
            #     self.mem = item
            print('\nkeys: {}'.format(super(odict, self).keys()))
            print('\n{}'.format(readline.get_line_buffer()), end='')
            # pprint would be nice here
        val = super(odict, self).__getitem__(item)
        if isList(val):
            return olist(val)
        elif isDict(val):
            return odict(val)
        elif isTuple(val):
            return otupl(val)
        return val
    def __getitem__(self, item):
        val = super(odict, self).__getitem__(item)
        if isList(val):
            return olist(val)
        elif isDict(val):
            return odict(val)
        elif isTuple(val):
            return otupl(val)
        return val
