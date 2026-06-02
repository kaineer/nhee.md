# NavbarData

from pathlib import Path


def split_subdir(subdir):
    parts = subdir.split("/")
    upper = lower = None
    if len(parts) > 0:
        upper = parts[0]
    if len(parts) > 1:
        lower = parts[1]
    return upper, lower


class NavbarItem:
    def __init__(self, subdir):
        upper, lower = split_subdir(subdir)
        self.upper = upper
        self.lower = lower


class NavbarData:
    def __init__(self, root):
        self.root = root

    def add_meta(self, meta_path):
        path = Path(meta_path).parent
        #
