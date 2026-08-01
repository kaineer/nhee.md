from kit.tag import tag
from page.types.params import Params

from j2.templates import TemplateContainer
from pathlib import Path

class List(Params):
    def build_parameters(self):
        render = TemplateContainer("jinja").template("page/list")
        self.set("items", render(
            self.context.data
        ))
