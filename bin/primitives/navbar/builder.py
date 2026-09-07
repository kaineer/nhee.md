from pathlib import Path

import yaml


class NavbarBuilder:
    def __init__(self, root):
        self.root = Path(root)
        self.items = []

    def build(self):
        self.items = []

        root_page = self._page(self.root)
        if root_page is None:
            return self

        self.items.append(self._item(root_page, url=""))

        for directory in self._children(self.root, root_page):
            page = self._page(directory)
            if page is None:
                continue

            item = self._item(page, url=directory.name)
            children = []
            for child in self._children(directory, page):
                child_page = self._page(child)
                if child_page is None:
                    continue
                children.append(self._item(child_page, url=child.name))
            if children:
                item["children"] = children
            self.items.append(item)

        return self

    def _children(self, directory, page):
        names = page.get("children", [])
        if type(names) is not list:
            return []

        result = []
        for name in names:
            if type(name) is not str:
                continue
            path = directory / name
            if path.is_dir():
                result.append(path)
        return result

    def _page(self, directory):
        meta_path = directory / "meta.yaml"
        if not meta_path.is_file():
            return None

        data = yaml.safe_load(meta_path.open().read())
        if type(data) is not dict:
            return None

        page = data.get("page", {})
        if type(page) is not dict:
            return None

        return page

    def _item(self, page, url):
        return {
            "title": page.get("slug", page.get("title", "")),
            "url": url,
        }
