from page.types.params import Params


class DoushiTable(Params):
    def build_parameters(self):
        self.params["doushi"] = self.context.data.get("doushi", [])
