"Some types to make dict objects easier to traverse"

isTuple = lambda e: isinstance(e, tuple)
isList = lambda e: isinstance(e, list)
isDict = lambda e: isinstance(e, dict)
isContainer = lambda e: any([isTuple(e), isList(e), isDict(e)])

class objTupl(tuple):
    def __getitem__(self, item):
        val = super(objTupl, self).__getitem__(item)
        if isList(val):
            return objList(val)
        elif isDict(val):
            return objDict(val)
        elif isTuple(val):
            return objTupl(val)
        return val

class objList(list):
    def __getitem__(self, item):
        val = super(objList, self).__getitem__(item)
        if isList(val):
            return objList(val)
        elif isDict(val):
            return objDict(val)
        elif isTuple(val):
            return objTupl(val)
        return val

class objDict(dict):
    def __getattr__(self, item):
        val = self.get(item)
        if isList(val):
            return objList(val)
        elif isDict(val):
            return objDict(val)
        elif isTuple(val):
            return objTupl(val)
        return val
    def __getitem__(self, item):
        val = self.get(item)
        if isList(val):
            return objList(val)
        elif isDict(val):
            return objDict(val)
        elif isTuple(val):
            return objTupl(val)
        return val
