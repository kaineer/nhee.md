class Params:
    def __init__(self, context):
        self.context = context
        self.params = {}
        self.build_parameters()

    def parameters(self):
        return self.params

    def set(self, key, value):
        self.params[key] = str(value)

    def build_parameters(self):
        raise NotImplementedError()
