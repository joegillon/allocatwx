import copy
import re


class Formatter(object):
    def __init__(self, *args, **kwargs):
        pass

    def validate(self, value):
        return True

    def format(self, value):
        return True

    def coerce(self, value):
        return True


class FormatterMeta(type):
    def __new__(cls, classname, bases, classdict):
        newdict = copy.copy(classdict)

        if Formatter in bases:
            def __init__(self, *args, **kwargs):
                Formatter.__init__(self, *args, **kwargs)
                initialize = getattr(self, 'initialize', None)
                if initialize:
                    initialize()
            newdict['__init__'] = __init__
        else:
            def __init__(self, *args, **kwargs):
                super(self.__class__, self).__init__(*args, **kwargs)
                initialize = getattr(self, 'initialize', None)
                if initialize:
                    initialize()
            newdict['__init__'] = __init__

        re_validation = newdict.get('re_validation', None)
        if re_validation:
            re_validation_flags = newdict.get('re_validation_flags', 0)
            newdict['_re_validation'] = re.compile(re_validation, re_validation_flags)
            def validate(self, value):
                return (self.re_validation.match(value) != None)
            newdict['validate'] = validate

        return type.__new__(cls, classname, bases, newdict)


class MonthFormatter(Formatter):
    re_validation = '^(0?[1-9]|1[012])/[0-9]{2}$'

    def format(self, value):
        return value[2:] + '/' + value[0:2]

    def coerce(self, value):
        return value[3:] + value[0:2]
