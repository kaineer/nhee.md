from page.types.params import Params


class List(Params):
    def build_parameters(self):
        # Список передаём как есть: set() приводит значения к str
        self.params["links"] = self.context.data.get("links", [])
