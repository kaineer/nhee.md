from pathlib import Path

import yaml
from attr import dataclass


def yaml_reader(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


@dataclass
class PageContext:
    title: str
    type: str
    subdir: str
    data: dict


#
class ContextLoader:
    def __init__(self, root, reader=yaml_reader):
        self.root = root
        self.reader = reader

    def load(self, path):
        data = self.reader(path)
        page_data = data.get("page", {})
        title = page_data.get("title", None)
        type = page_data.get("type", None)

        subdir = Path(path).parent.relative_to(self.root)

        return PageContext(title=title, subdir=str(subdir), type=type, data=data)
