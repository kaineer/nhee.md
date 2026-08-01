from kit.tag import tag
from page.types.params import Params

from j2.templates import TemplateContainer
from pathlib import Path

class List(Params):
    def build_parameters(self):
        render = self.template("page/list")
        data = self.context.data
        self.set("items", render(data))
