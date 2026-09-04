from page.types.params import Params

class Kanji(Params):
    def build_parameters(self):
        # Список передаём как есть: set() приводит значения к str
        self.params["kanji"] = self.context.data.get("kanji", [])
