from kit.tag import tag
from page.types.params import Params


class List(Params):
    # <div class="prompts-list">
    #        <a class='prompt-item' href='https://chat.deepseek.com/'>       <div class='prompt-title'>Deepseek</div>       <div class='prompt-description'>Into the unknown</div>     </a>      <a class='prompt-item' href='https://yandex.ru/alice/'>       <div class='prompt-title'>Alice AI</div>       <div class='prompt-description'>Чем помочь сегодня?</div>     </a>      <a class='prompt-item' href='https://shedevrum.ai/text-to-image/'>       <div class='prompt-title'>Шедеврум</div>       <div class='prompt-description'>Создать изображение</div>     </a>      <a class='prompt-item' href='https://www.kimi.com/chat/'>       <div class='prompt-title'>KIMI</div>       <div class='prompt-description'>Kimi chat</div>     </a>
    # </div>
    def item(self, url, title, description=""):
        return tag(
            "a",
            attr={"href": url},
            classname="prompt-item",
            children=[
                tag("div", classname="prompt-title", children=title),
                tag("div", classname="prompt-description", children=description),
            ],
        )

    def build_list(self):
        tags = []
        for link in self.context.data["links"] or []:
            tags.append(self.item(link["url"], link["title"], link["description"]))
        self.set("items", tag("ul", children=tags))

    def build_parameters(self):
        self.build_list()
