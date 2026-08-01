from j2.templates import TemplateContainer

class Params:
    def __init__(self, context):
        self.context = context
        self.params = {}
        self.templates = TemplateContainer("jinja")
        self.build_parameters()

    def parameters(self):
        return self.params

    def set(self, key, value):
        self.params[key] = str(value)

    def template(self, name):
        return self.templates.template(name)

    def build_parameters(self):
        raise NotImplementedError()
