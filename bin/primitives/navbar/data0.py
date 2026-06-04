# NavbarData

from pathlib import Path

from primitives.subdir import subdir


def split_subdir(subdir):
    parts = subdir.split("/")
    upper = lower = None
    if len(parts) > 0:
        upper = parts[0]
        if upper == ".":
            upper = None
    if len(parts) > 1:
        lower = parts[1]
    return upper, lower


root_path = "/"


def build_path(upper, lower):
    path = root_path
    if upper is not None:
        path += upper + "/"
        if lower is not None:
            path += lower + "/"
    return path


class NavbarItem:
    def __init__(self, subdir):
        upper, lower = split_subdir(subdir)
        self.upper = upper
        self.lower = lower
        self.path = build_path(upper, lower)
        self.title = None

    def __repr__(self):
        return f"NavbarItem: {self.path}"


class NavbarData:
    def __init__(self, root):
        self.root = root
        self.items = []
        self.upper = []
        self.titles = None

    def set_titles(self, titles):
        self.titles = titles

    def _add_upper_label(self, item):
        upper = item.upper
        found = next((up for up in self.upper if upper == up), -1)
        if found == -1:
            self.upper.append(upper)

    def _find_by_path(self, path):
        if path == ".":
            path = root_path

        found = next((it for it in self.items if path == it.path), None)
        return found

    def _add_meta_item(self, item):
        found = self._find_by_path(item.path)
        if found is None:
            self.items.append(item)
            self._add_upper_label(item)
            return item
        return found

    def _is_metapath(self, path):
        return path.endswith("meta.yaml")

    def _get_relative_path(self, path):
        path = path or ""
        if self._is_metapath(path):
            return str(Path(path).parent.relative_to(self.root))
        return path

    def add_meta(self, meta_path):
        path = self._get_relative_path(meta_path)
        item = self._add_meta_item(NavbarItem(path))

        return item

    def find_current(self, meta_path):
        path = self._get_relative_path(meta_path)
        path = subdir(path, 2)

        found = self._find_by_path(path)

        return found

    def find_upper(self, meta_path):
        path = self._get_relative_path(meta_path)
        path = subdir(path, 1)

        found = self._find_by_path(path)

        if self.titles is not None and found is not None:
            if found.path in self.titles:
                found.title = self.titles[found.path]

        return found

    def find_lower(self, meta_path):
        path = str(Path(meta_path).parent.relative_to(self.root))
        path = subdir(path, 2)

        found = self._find_by_path(path)
        if found is not None:
            if type(found.lower) is str:
                return found

        return None

    def find_all_lower(self, path):
        parts = path.split("/")
        upper_item = parts[0]

        navbar_items = [
            item
            for item in self.items
            if item.upper == upper_item and item.lower is not None
        ]

        for item in navbar_items:
            if self.titles is not None:
                if item.path in self.titles:
                    item.title = self.titles[item.path]

        return navbar_items
