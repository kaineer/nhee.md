from dataclasses import dataclass


@dataclass
class PageContext:
    root: str  # project root
    subdir: str  # current page subdir
    type: str  # page type
    title: str  # page title
