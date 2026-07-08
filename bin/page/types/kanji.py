from kit.tag import tag
from page.types.params import Params

class Kanji(Params):
    def build_example(self, example):
        kanji = example.get("kanji", "")
        reading = example.get("reading", "")
        meaning = example.get("meaning", "")

        combined_example = f"{kanji} = {reading}"

        return tag("li", children=[
            combined_example, 
            tag("span", children=[f"{meaning}"])
        ])

    def build_item(self, item):
        char = item.get("char", "")
        reading = item.get("reading", "")
        meaning = item.get("meaning", "")
        examples = item.get("examples", [])

        examples_html = "".join([self.build_example(e) for e in examples])

        return tag(
            "div",
            classname="kanji-item",
            children=[
                tag(
                    "div",
                    classname="kanji-front",
                    children=[
                        tag("div", classname="kanji-char", children=[char]),
                        tag("div", classname="kanji-reading", children=[reading]),
                        tag("div", classname="kanji-translation", children=[meaning])
                    ]
                ),
                tag(
                    "div",
                    classname="kanji-back",
                    children=[
                        tag("ul", children=examples_html)
                    ],
                )
            ]
        )
        
    def build_parameters(self):
        """
        Генерирует HTML-разметку для списка карточек иероглифов 
        и подставляет её в шаблон вместо %kanji.items%.
        """
        # Получаем данные из meta.yaml через self.context.data
        page_data = self.context.data.get("page", {})
        kanji_list = self.context.data.get("kanji", [])
        
        # Если список иероглифов пуст, просто возвращаем пустую строку
        if not kanji_list:
            self.set("kanji.items", "")
            return

        full_html = "\n".join([self.build_item(it) for it in kanji_list])

        # Передаем результат в плейсхолдер %kanji.items%
        self.set("kanji.items", full_html)
