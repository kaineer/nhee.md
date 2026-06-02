from tag import tag
from pathlib import Path

stylesheet_attr = {
    "rel": "stylesheet", 
    "type": "text/css"
}

def style(name, page_context):
    return tag("link", attr={
        **stylesheet_attr,
        "href": Path(page_context.root) / "assets" / (name + ".css")
    })
