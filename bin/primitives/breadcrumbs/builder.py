from pathlib import Path

import yaml

from primitives.subdir import subdir


class BreadcrumbsBuilder:
    """Sibling lists from the current page up to the navbar-covered prefix."""

    def __init__(self, root):
        self.root = Path(root)
        self.pages = {}
        self.children = {}
        self.nav_root = []
        self.nav_lower = {}

    def build(self):
        self.pages = {}
        self.children = {}
        self.nav_root = []
        self.nav_lower = {}

        root_page = self._page(self.root)
        self.nav_root = self._declared_names(root_page)
        self._index_directory(self.root)
        return self

    def context(self, ctx):
        parts = self._parts(ctx.subdir)
        covered = self._covered_segments(parts)
        levels = []

        for depth in range(covered + 1, len(parts) + 1):
            prefix = "/".join(parts[:depth])
            if prefix not in self.pages:
                continue

            parent = "/".join(parts[:depth - 1])
            current_name = parts[depth - 1]
            names = self.children.get(parent, [])
            items = []
            current_idx = None

            for name in names:
                rel = name if parent == "" else f"{parent}/{name}"
                page = self.pages.get(rel)
                if page is None:
                    continue
                is_current = name == current_name
                if is_current:
                    current_idx = len(items)
                items.append(
                    {
                        "url": self._view_url(rel, ctx),
                        "slug": page["slug"],
                        "current": is_current,
                        "next": False,
                    }
                )

            if current_idx is not None and current_idx + 1 < len(items):
                items[current_idx + 1]["next"] = True

            if items:
                levels.append(items)

        return {"crumb_levels": levels}

    def _index_directory(self, directory):
        rel = self._rel(directory)
        page = self._page(directory)
        if page is not None:
            fallback = directory.name if rel else "Home"
            self.pages[rel] = {"slug": self._slug(page, fallback)}
            if rel and "/" not in rel:
                self.nav_lower[rel] = self._declared_names(page)

        self.children[rel] = self._child_page_names(directory, page)

        for child in sorted(directory.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                self._index_directory(child)

    def _covered_segments(self, parts):
        if not parts:
            return 0
        if parts[0] not in self.nav_root:
            return 0
        if len(parts) >= 2 and parts[1] in self.nav_lower.get(parts[0], []):
            return 2
        return 1

    def _child_page_names(self, directory, page):
        declared = []
        for name in self._declared_names(page):
            child = directory / name
            if child.is_dir() and self._page(child) is not None:
                declared.append(name)

        extras = []
        for child in sorted(directory.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if child.name in declared:
                continue
            if self._page(child) is not None:
                extras.append(child.name)

        return declared + extras

    def _view_url(self, rel, ctx):
        abs_url = subdir(rel)
        if ctx.web:
            return abs_url
        return abs_url + "index.html"

    def _slug(self, page, fallback):
        slug = page.get("slug") or page.get("title") or ""
        return slug if slug else fallback

    def _declared_names(self, page):
        if type(page) is not dict:
            return []
        entries = page.get("children", [])
        if type(entries) is not list:
            return []
        return [
            entry
            for entry in entries
            if type(entry) is str and entry != "."
        ]

    def _parts(self, path):
        if path is None or path in ("", "."):
            return []
        return path.split("/")

    def _rel(self, directory):
        rel = directory.resolve().relative_to(self.root.resolve())
        text = rel.as_posix()
        if text == ".":
            return ""
        return text

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
