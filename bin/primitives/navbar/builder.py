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

        for entry in self._entries(root_page):
            item = self._resolve_entry(self.root, entry, with_children=True)
            if item is not None:
                self.items.append(item)

        return self

    def _entries(self, page):
        entries = page.get("children", [])
        if type(entries) is not list:
            return []

        result = []
        for entry in entries:
            if type(entry) is str or type(entry) is dict:
                result.append(entry)
        return result

    def _resolve_entry(self, directory, entry, with_children=False):
        if type(entry) is dict:
            return self._item_from_object(entry)

        if type(entry) is not str:
            return None

        path = directory / entry
        if not path.is_dir():
            return None

        page = self._page(path)
        if page is None:
            return None

        item = self._item(page, url=path.name)
        if with_children:
            children = []
            for child_entry in self._entries(page):
                child_item = self._resolve_entry(path, child_entry)
                if child_item is not None:
                    children.append(child_item)
            if children:
                item["children"] = children
        return item

    def _item_from_object(self, entry):
        return {
            "title": entry.get("slug", ""),
            "url": entry.get("url", ""),
        }

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
