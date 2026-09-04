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
from primitives.template.template_container import TemplateContainer
from j2.templates import TemplateContainer as J2Templates
from widgets.navbar import build_navbar, navbar_context

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
        self.j2 = J2Templates("jinja")
        self.context_loader = ContextLoader(root)
        self.navbar_data = NavbarData(str(Path(root) / "navbar.yaml"))

    def _j2_page_template(self, type):
        name = f"pages/{type}"
        path = Path("jinja") / f"{name}.j2"
        if path.is_file():
            return self.j2.template(name)
        return None

    def build_page(self, file):
        context = self.context_loader.load(file)
        type = context.type
        title = context.title
        page_class = page_types[type]
        parameters = page_class(context).parameters()

        j2_render = self._j2_page_template(type)
        if j2_render is not None:
            nav_ctx = navbar_context(context, self.navbar_data)
            mappings = {
                **nav_ctx,
                **parameters,
                "root": context.root,
                "title": title,
                "page": {"title": title},
            }
            return j2_render(mappings)

        navbar = build_navbar(context, self.navbar_data)
        mappings = {
            "navbar": navbar,
            **parameters,
            "root": context.root,
            "title": title,
        }
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
