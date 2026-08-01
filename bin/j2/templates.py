import jinja2
from pathlib import Path

class TemplateContainer:
    def __init__(self, path):
        self.path = path

    def template(self, name):
        path = Path(self.path).absolute() / (name + ".j2")
        content = path.read_text()

        template = jinja2.Template(content)

        def render_template(obj):
            return template.render(obj) 

        return render_template

