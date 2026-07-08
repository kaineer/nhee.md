from page.types.params import Params

class Cite(Params):
    def build_parameters(self):
        page = self.context.data.get("page", {})
        content = page.get("content", "")
        self.set("content", content)
