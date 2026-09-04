from kit.tag import tag
from primitives.subdir import subdir
from jinja2 import Template

hamburger = "Home"

def render_template(source, obj):
    template = Template(source)
    return template.render(obj)

def navbar_item(url, title, ctx, current=False):
    _classname = ""
    if current:
        _classname = "active"

    return render_template(
        "<li><a class='{{ classname }}' href='{{ root }}{{ url }}'>{{ title }}</a></li>", {
            "url": url,
            "title": title,
            "classname": _classname,
            "root": ctx.root,
        }
    )

def upper_navbar_link(ni, ctx):
    url = ni.url
    title = ni.title or ni.upper or hamburger
    current = subdir(ctx.subdir, 1) == ni.url
    if not ctx.web:
        url += "index.html"
    return navbar_item(url, title, ctx, current)


def lower_navbar_link(ni, ctx):
    url = ni.url
    title = ni.title or ni.lower
    current = subdir(ctx.subdir, 2) == ni.url
    if not ctx.web:
        url += "index.html"
    return navbar_item(url, title, ctx, current)


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
    navbars = [
        upper_navbar(context, navbar_data),
    ]
    if len(navbar_data.find_all_lower(context.subdir)) > 0:
        navbars.append(lower_navbar(context, navbar_data))
    return tag("div", classname="navbar", children=navbars)


def _item_url(ni, ctx):
    url = ni.url
    if not ctx.web:
        url += "index.html"
    return url


def navbar_context(context, navbar_data):
    upper_items = [
        {
            "url": _item_url(navbar_data.find_upper(item), context),
            "title": navbar_data.find_upper(item).title or navbar_data.find_upper(item).upper or hamburger,
            "current": subdir(context.subdir, 1) == navbar_data.find_upper(item).url,
        }
        for item in navbar_data.upper
    ]
    lower_items = [
        {
            "url": _item_url(ni, context),
            "title": ni.title or ni.lower,
            "current": subdir(context.subdir, 2) == ni.url,
        }
        for ni in navbar_data.find_all_lower(context.subdir)
    ]
    return {"upper_items": upper_items, "lower_items": lower_items}
