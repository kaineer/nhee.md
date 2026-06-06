from pathlib import Path

import yaml
from attr import dataclass


def yaml_reader(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def file_reader(path):
    if Path(path).is_file():
        return Path(path).open().read()
    return ""


@dataclass
class PageContext:
    title: str
    type: str
    root: str
    subdir: str
    data: dict
    body_content: str


#
class ContextLoader:
    def __init__(self, root, reader=yaml_reader, fs_reader=file_reader):
        self.root = root
        self.reader = reader
        self.fs_reader = fs_reader

    def load(self, path):
        data = self.reader(path)
        page_data = data.get("page", {})
        title = page_data.get("title", None)
        type = page_data.get("type", None)

        markdown_file = str(Path(path).parent / "meta.md")
        body_content = self.fs_reader(markdown_file)

        subdir = str(Path(path).parent.relative_to(self.root))

        if subdir is None or subdir == "" or subdir == ".":
            root = "."
        else:
            root = "/".join([".."] * len(subdir.split("/")))

        return PageContext(
            title=title,
            subdir=str(subdir),
            type=type,
            data=data,
            root=root,
            body_content=body_content,
        )
