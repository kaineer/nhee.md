from page.types.params import Params
from cmarkgfm import markdown_to_html

class Markdown(Params):
    def build_parameters(self):
        self.set("content", markdown_to_html(self.context.body_content))

