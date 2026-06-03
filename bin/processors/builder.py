from pathlib import Path

from page.types.clip import Clip
from page.types.list import List
from page.types.markdown import Markdown
from primitives.context.data import ContextLoader
from primitives.navbar.data import NavbarData
from primitives.page_enumerate import find_meta_files
from primitives.template.template_container import TemplateContainer
from widgets.navbar import build_navbar

page_types = {"list": List, "markdown": Markdown, "clip": Clip}


class Builder:
    def __init__(self, root):
        self.root = root
        templates_root = str(Path(root) / "templates")
        self.templates = TemplateContainer(templates_root)
        self.context_loader = ContextLoader(root)
        self.navbar_data = NavbarData(self.root)

    def build(self):
        meta_files = find_meta_files(self.root)
        for file in meta_files:
            self.navbar_data.add_meta(file)
        for file in meta_files:
            context = self.context_loader.load(file)
            navbar = build_navbar(context, self.navbar_data)
            type = context.type
            template = self.templates.get(type)
            page_class = page_types[type]
            parameters = page_class(context)
            page = str(
                template.apply({"navbar": navbar, "root": self.root, **parameters})
            )

            print(page)
            # Write to Path(self.root) / context.subdir / "index.html"
            # content of page
