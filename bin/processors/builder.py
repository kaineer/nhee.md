from pathlib import Path

import yaml
from page.types.cite import Cite
from page.types.list import List
from page.types.markdown import Markdown
from page.types.kanji import Kanji
from page.types.dummy import Dummy

from primitives.context.data import ContextLoader
from primitives.navbar.data import NavbarData
from primitives.page_enumerate import find_meta_files
from jinja2 import Template
from primitives.template.template_container import TemplateContainer
from widgets.navbar import build_navbar

page_types = {
    "list": List, 
    "cite": Cite, 
    "markdown": Markdown,
    "kanji": Kanji,
    "repos": Dummy
}

class Builder:
    def __init__(self, root):
        self.root = root
        templates_root = str(Path(root) / "templates")
        self.templates = TemplateContainer(templates_root)
        self.context_loader = ContextLoader(root)
        self.navbar_data = NavbarData(str(Path(root) / "navbar.yaml"))

    def _jinja_page_template(self, type):
        path = Path("jinja") / "pages" / f"{type}.html.j2"
        if not path.is_file():
            return None
        return Template(path.read_text())

    def build_page(self, file):
        context = self.context_loader.load(file)
        navbar = build_navbar(context, self.navbar_data)
        type = context.type
        title = context.title
        page_class = page_types[type]
        parameters = page_class(context).parameters()
        mappings = {
            "navbar": navbar,
            **parameters,
            "root": context.root,
            "title": title,
        }
        jinja_template = self._jinja_page_template(type)
        if jinja_template is not None:
            return jinja_template.render({**mappings, "page": {"title": title}})
        template = self.templates.get(type)
        page = str(template.apply(mappings))
        return page

    def build(self):
        meta_files = find_meta_files(self.root)
        for file in meta_files:
            basename = file[len(self.root) + 1:]
            print(f"\r * Building {basename}..", end="", flush=True)
            try:
                page = self.build_page(file)
                outfile = Path(file).parent / "index.html"
                outfile.open("w").write(page)
                print("done", end=(" " * 80), flush=True)
            except Exception as e:
                print("fail")
                print(e)
                traceback.print_exc()
                exit(1)
        print("")
