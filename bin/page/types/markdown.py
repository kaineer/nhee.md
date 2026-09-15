import html

from page.types.params import Params
from cmarkgfm import markdown_to_html


class Markdown(Params):
    def build_parameters(self):
        source = self.context.body_content or ""
        copy = self._copy_enabled()
        self.params["copy"] = copy
        self.set("content", markdown_to_html(source))
        if copy:
            self.set("source", html.escape(source))

    def _copy_enabled(self):
        page = self.context.data.get("page", {}) or {}
        value = page.get("copy", True)
        if value is False or value is None:
            return False
        if isinstance(value, str) and value.strip().lower() in ("false", "no", "0"):
            return False
        return bool(value)

