from kit.tag import tag
from primitives.subdir import subdir

hamburger = "Home"


def navbar_item(url, title, current=False):
    _classname = None
    if current:
        _classname = "active"
    return tag(
        "li",
        children=[
            tag(
                "a", classname=_classname, attr={"href": "%root%" + url}, children=title
            )
        ],
    )


def upper_navbar_link(ni, ctx):
    url = ni.path
    title = ni.title or ni.upper or hamburger
    current = subdir(ctx.subdir, 1) == ni.path
    return navbar_item(url, title, current)


def lower_navbar_link(ni, ctx):
    url = ni.path
    title = ni.title or ni.lower
    current = subdir(ctx.subdir, 2) == ni.path
    return navbar_item(url, title, current)


def upper_navbar(context, navbar_data):
    upper = navbar_data.upper
    children = [
        upper_navbar_link(navbar_data.find_upper(item), context) for item in upper
    ]
    return tag("ul", classname="nav-primary", children=children)


def lower_navbar(context, navbar_data):
    children = [
        lower_navbar_link(item, context)
        for item in navbar_data.find_all_lower(context.subdir)
    ]
    return tag("ul", classname="nav-secondary", children=children)


def build_navbar(context, navbar_data):
    return tag(
        "div",
        classname="navbar",
        children=[
            upper_navbar(context, navbar_data),
            lower_navbar(context, navbar_data),
        ],
    )
