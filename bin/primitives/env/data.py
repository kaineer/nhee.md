import os

_environ = os.environ


class Env:
    def __getattribute__(self, name):
        key = name.upper()
        if key in _environ:
            return _environ[key]
        return ""
