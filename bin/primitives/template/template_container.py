from pathlib import Path

from primitives.template.template import Template


class TemplateContainer:
    def __init__(self, root):
        self.root = root
        self.templates = {}

    def get(self, template_name):
        if template_name in self.templates:
            return self.templates[template_name]

        path = Path(self.root) / (template_name + ".html")

        template = Template(path.open().read())
        self.templates[template_name] = template

        return template
