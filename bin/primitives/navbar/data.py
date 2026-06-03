# NavbarData

from pathlib import Path


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

    def __repr__(self):
        return f"NavbarItem: {self.path}"


class NavbarData:
    def __init__(self, root):
        self.root = root
        self.items = []
        self.upper = []

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

    def add_meta(self, meta_path):
        path = str(Path(meta_path).parent.relative_to(self.root))
        item = self._add_meta_item(NavbarItem(path))

        return item

    def find_current(self, meta_path):
        path = str(Path(meta_path).parent.relative_to(self.root))
        if path == ".":
            path = root_path
        else:
            parts = path.split("/")
            path = "/".join(parts[0:2])
            path = f"/{path}/"

        found = self._find_by_path(path)

        return found
