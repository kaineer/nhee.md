from ..kit.tag import tag

hamburger = "󰍜"

# def upper_item(item, current):
#     link = tag("a", attr={"href": item}, children=item)
#     cn = ""
#     if current:
#         cn = "current"
#     return tag("li", classname=cn, children=(link or hamburger))
#
#
# def upper_navbar(items, current=None):
#     return "".join([upper_item(item, current) for item in items])


def navbar_item(url, title):
    return tag("li", children=[tag("a", {"href": url}, children=title)])


def upper_navbar(context, navbar_data):
    upper = navbar_data.upper
    return tag("div", classname="nav-primary", children=[])


def lower_navbar(context, navbar_data):
    pass


def build_navbar(context, navbar_data):
    return tag(
        "div",
        classname="navbar",
        children=[
            upper_navbar(context, navbar_data),
            lower_navbar(context, navbar_data),
        ],
    )
