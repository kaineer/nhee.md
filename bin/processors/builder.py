from pathlib import Path

import yaml
from page.types.cite import Cite
from page.types.list import List

# from page.types.markdown import Markdown
from primitives.context.data import ContextLoader
from primitives.navbar.data import NavbarData
from primitives.page_enumerate import find_meta_files
from primitives.template.template_container import TemplateContainer
from widgets.navbar import build_navbar

page_types = {"list": List, "cite": Cite}


class Builder:
    def __init__(self, root):
        self.root = root
        templates_root = str(Path(root) / "templates")
        self.templates = TemplateContainer(templates_root)
        self.context_loader = ContextLoader(root)
        self.navbar_data = NavbarData(self.root)
        titles = yaml.safe_load((Path(root) / "titles.yaml").open().read())
        self.navbar_data.set_titles(titles)

    def build(self):
        meta_files = find_meta_files(self.root)
        for file in meta_files:
            self.navbar_data.add_meta(file)
        for file in meta_files:
            print(" * Building ", file)
            context = self.context_loader.load(file)
            navbar = build_navbar(context, self.navbar_data)
            type = context.type
            title = context.title
            template = self.templates.get(type)
            page_class = page_types[type]
            parameters = page_class(context).parameters()
            page = str(
                template.apply(
                    {
                        "navbar": navbar,
                        **parameters,
                        "root": context.root,
                        "title": title,
                    }
                )
            )

            outfile = Path(file).parent / "index.html"
            outfile.open("w").write(page)
