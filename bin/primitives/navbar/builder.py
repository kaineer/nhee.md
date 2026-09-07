from pathlib import Path

import yaml

from primitives.subdir import subdir

HOME_TITLE = "Home"


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

    def context(self, ctx):
        upper_items = []
        current_upper = None
        current_abs = None
        current_key = self._upper_key(ctx)

        for item in self.items:
            abs_url = self._abs_url(item)
            upper_items.append(self._view_item(item, abs_url, ctx, level=1))
            if item.get("url", "") == current_key:
                current_upper = item
                current_abs = abs_url

        lower_items = []
        if current_upper is not None:
            for child in current_upper.get("children", []):
                abs_url = self._abs_url(child, parent_url=current_abs)
                lower_items.append(self._view_item(child, abs_url, ctx, level=2))

        return {"upper_items": upper_items, "lower_items": lower_items}

    def _upper_key(self, ctx):
        path = ctx.subdir
        if path is None or path in ("", "."):
            return ""
        return path.split("/")[0]

    def _abs_url(self, item, parent_url=None):
        url = item.get("url", "")
        if parent_url is None:
            if url == "":
                return "/"
            return f"/{url}/"
        return f"{parent_url}{url}/"

    def _view_item(self, item, abs_url, ctx, level):
        title = item.get("title", "")
        if not title:
            title = HOME_TITLE if level == 1 else item.get("url", "")
        return {
            "url": abs_url if ctx.web else abs_url + "index.html",
            "title": title,
            "current": subdir(ctx.subdir, level) == abs_url,
        }

    def _entries(self, page):
        entries = page.get("children", [])
        if type(entries) is not list:
            return []

        return [entry for entry in entries 
            if type(entry) in [str, dict]
        ]

    def _resolve_entry(self, directory, entry, with_children=False):
        if type(entry) is dict:
            return self._item_from_object(entry)

        if type(entry) is not str:
            return None

        if entry == ".":
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
