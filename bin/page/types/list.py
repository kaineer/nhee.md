from kit.tag import tag
from page.types.params import Params

from j2.templates import TemplateContainer
from pathlib import Path

"""
--- item
<a href="{{ url }}" class="prompt-item">
  <div class="prompt-title">{{ title }}</div>
  <div class="prompt-description">{{ description }}</div>
</a>

--- links
<ul>
  {% for link in links %}
  <a href="{{ link.url }}" class="prompt-item">
    <div class="prompt-title">{{ link.title }}</div>
    <div class="prompt-description">{{ 
      link.description 
    }}</div>
  </a>
  {% endfor %}
</ul>
"""


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
        render = TemplateContainer("jinja").template("page/list")
        self.set("items", render(
            self.context.data
        ))

        # self.build_list()
