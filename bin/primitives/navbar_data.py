from pathlib import Path


class NavbarItem:
    def __init__(self, relative_path):
        dirname = str(Path(relative_path).parent)
        if dirname == ".":
            dirname = ""
        parts = dirname.split("/")
        self.upper = None
        if len(parts) > 0:
            self.upper = parts[0]
        self.lower = None
        if len(parts) > 1:
            self.lower = parts[1]

    def __str__(self):
        return f"[upper={self.upper}, lower={self.lower}]"


class NavbarData:
    def __init__(self, root):
        self.root = root
        self.meta_files = []

    def add(self, meta_file):
        relative_path = str(Path(meta_file).relative_to(self.root))
        self.meta_files.append(NavbarItem(relative_path))

    def __str__(self) -> str:
        return ", ".join([str(data) for data in self.meta_files])


def build_navbar_data(meta_files, root):
    navbar_data = NavbarData(root)
    for meta_file in meta_files:
        navbar_data.add(meta_file)
    return navbar_data
