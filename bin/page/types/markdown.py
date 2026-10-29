import html

from page.types.params import Params
from cmarkgfm import Options, markdown_to_html


class Markdown(Params):
    def build_parameters(self):
        source = self.context.body_content or ""
        copy = self._flag("copy", default=True)
        raw = self._flag("raw", default=False)
        options = Options.CMARK_OPT_UNSAFE if raw else 0
        self.params["copy"] = copy
        self.set("content", markdown_to_html(source, options=options))
        if copy:
            self.set("source", html.escape(source))

    def _flag(self, name, default=False):
        page = self.context.data.get("page", {}) or {}
        value = page.get(name, default)
        if value is False or value is None:
            return False
        if isinstance(value, str) and value.strip().lower() in ("false", "no", "0"):
            return False
        return bool(value)

