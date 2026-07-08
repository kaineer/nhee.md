from kit.tag import tag
from page.types.params import Params

class Kanji(Params):
    def build_item(self, item, examples_html):
        char = item.get("char", "")
        reading = item.get("reading", "")
        meaning = item.get("meaning", "")

        return tag(
            "div",
            classname="kanji-item",
            children=[
                tag(
                    "div",
                    classname="kanji-front",
                    children=[
                        tag("div", classname="kanji-char", char),
                        tag("div", classname="kanji-reading", reading),
                        tag("div", classname="kanji-translation", meaning)
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

        pass
        
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

        # Генерируем HTML для каждой карточки
        items_html = []
        for item in kanji_list:
            # Формируем список примеров
            examples_html = ""
            for ex in item.get("examples", []):
                kanji_text = ex.get("kanji", "")
                reading_text = ex.get("reading", "")
                meaning = ex.get("meaning", "")
                
                # Собираем строку вида "住まい = すまい"
                combined_example = f"{kanji_text} = {reading_text}"
                
                examples_html += f'<li>{combined_example} <span style="color: #81a1c1;">({meaning})</span></li>'

            # Собираем одну карточку
            block = f"""
            <div class="kanji-item">
                <div class="kanji-front">
                    <div class="kanji-char">{item.get('char', '')}</div>
                    <div class="kanji-reading">{item.get('readings', '')}</div>
                    <div class="kanji-translation">{item.get('meaning', '')}</div>
                </div>
                <div class="kanji-back">
                    <ul>
                        {examples_html}
                    </ul>
                </div>
            </div>
            """
            items_html.append(block)

        # Объединяем все карточки в одну строку
        full_html = "\n".join(items_html)
        
        # Передаем результат в плейсхолдер %kanji.items%
        self.set("kanji.items", full_html)
