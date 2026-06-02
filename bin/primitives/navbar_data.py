from pathlib import Path

from primitives.page_context import create_page_context

def split_relative_path(path):
    dirname = str(Path(path).parent)
    if dirname == ".":
        dirname = ""
    parts = dirname.split("/")
    upper = None
    if len(parts) > 0:
        upper = parts[0]
    lower = None
    if len(parts) > 1:
        lower = parts[1]

    return upper, lower


class NavbarItem:
    def __init__(self, relative_path):
        upper, lower = split_relative_path(relative_path)
        self.path = relative_path
        self.upper = upper
        self.lower = lower

        self.title = None

        self.filepath = upper
        if lower is not None:
            self.filepath = str(Path(upper) / lower)


class NavbarData:
    def __init__(self, root):
        self.root = root
        self.meta_files = []
        self.upper = []

    def add(self, meta_file):
        relative_path = str(Path(meta_file).relative_to(self.root))
        ni = NavbarItem(relative_path)
        self.meta_files.append(ni)
        if ni.upper not in self.upper:
            self.upper.append(ni.upper)

        return ni

    def title(self, upper, lower=None):
        if lower is None:
            return self.find(upper)[0].title
        found = self.find(upper)
        item = [f for f in found if f.lower == lower][0]
        return item.title

    def find(self, upper_level):
        return [file for file in self.meta_files if file.upper == upper_level]


def build_navbar_data(meta_files, root):
    navbar_data = NavbarData(root)
    for meta_file in meta_files:
        ni = navbar_data.add(meta_file)
        ct = create_page_context(root, meta_file)
        ni.title = ct.title
    return navbar_data


__all__ = ["build_navbar_data"]
