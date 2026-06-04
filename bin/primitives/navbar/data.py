from pathlib import Path

import yaml


class NavbarItem:
    def __init__(self, obj, parent=None):
        self.upper = None
        self.lower = None
        self.title = obj.get("title", "")
        if parent is None:
            self.url = obj.get("url", "")
            if self.url == "":
                self.url = "/"
            else:
                self.upper = self.url
                self.url = f"/{self.url}/"
        else:
            url = obj.get("url", "")
            self.url = f"{parent.url}{url}/"
            self.upper = parent.upper
            if parent.lower is None:
                self.lower = url
            else:
                self.lower = parent.lower


class NavbarData:
    def __init__(self, path):
        data = yaml.safe_load(Path(path).open().read())

        self.items = []
        self.upper = []
        self.load_items(data)

    def load_items(self, data, parent=None):
        for item in data:
            children = item.get("children", [])
            nbi = NavbarItem(item, parent)
            if parent is None:
                self.upper.append(nbi.upper)
            self.items.append(nbi)
            self.load_items(children, nbi)

    def find_upper(self, upper):
        item = next(
            (it for it in self.items if it.upper == upper and it.lower is None), None
        )

        return item

    def find_all_lower(self, path):
        parts = path.split("/")
        upper_item = parts[0]

        return [
            item
            for item in self.items
            if item.upper == upper_item and item.lower is not None
        ]
