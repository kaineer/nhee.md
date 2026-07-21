def is_scalar(obj):
    return (
        type(obj) in [str, int, bool]
    )

class Meta:
    def __init__(self, obj = None):
        if obj is None:
            self._obj = {}
            self._none = True
        else:
            if type(obj) != dict:
                raise Exception("Meta content should be a dict")
            self._obj = obj

    def is_none(self):
        return self._none

    def __eq__(self, other):
        return (
            (self._none and (other is None)) or
            self == other
        )

    def __getattr__(self, name):
        value = self._obj.get(name, None)

        if is_scalar(value):
            return value
        return Meta(value)

def meta(path):
    pass
