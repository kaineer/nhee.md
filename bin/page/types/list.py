from kit.tag import tag
from page.types.params import Params

class List(Params):
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
