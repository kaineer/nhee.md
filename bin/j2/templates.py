import jinja2
from pathlib import Path


class TemplateContainer:
    def __init__(self, path):
        self.path = str(Path(path).absolute())
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.path),
            autoescape=False,
        )

    def template(self, name):
        template = self.env.get_template(name + ".j2")

        def render_template(obj):
            return template.render(obj)

        return render_template
