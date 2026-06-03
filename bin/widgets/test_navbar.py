from primitives.navbar.data import NavbarData
from widgets.navbar import build_navbar, lower_navbar, navbar_item, upper_navbar


def get_navbar_data():
    nb = NavbarData("/a")
    nb.add_meta("/a/meta.yaml")
    nb.add_meta("/a/b/meta.yaml")
    nb.add_meta("/a/b/c/meta.yaml")
    nb.add_meta("/a/b/d/meta.yaml")
    return nb


def lines(ll):
    return "".join(ll)


class MockCtx:
    def __init__(self, title, subdir, type="list", data={}):
        self.title = title
        self.subdir = subdir
        self.type = type
        self.data = data


def test_navbar_item():
    assert navbar_item("#hash", "hello") == '<li><a href="#hash">hello</a></li>'
    assert navbar_item("#hash", "hello", True) == (
        '<li><a class="current" href="#hash">hello</a></li>'
    )


def test_upper_navbar():
    nb = get_navbar_data()
    nb.set_titles({"/b/": "About"})
    ctx = MockCtx("Hello there", "")

    assert upper_navbar(ctx, nb) == lines(
        [
            '<ul class="nav-primary">',
            '<li><a class="current" href="/">󰍜</a></li>',
            '<li><a href="/b/">About</a></li>',
            "</ul>",
        ]
    )


def test_upper_navbar_about():
    nb = get_navbar_data()
    nb.set_titles({"/b/": "About"})
    ctx = MockCtx("About", "b")

    assert upper_navbar(ctx, nb) == lines(
        [
            '<ul class="nav-primary">',
            '<li><a href="/">󰍜</a></li>',
            '<li><a class="current" href="/b/">About</a></li>',
            "</ul>",
        ]
    )


def test_lower_bar():
    nb = get_navbar_data()
    nb.set_titles({"/b/c/": "First", "/b/d/": "Second"})
    ctx = MockCtx("First", "b/c")
    assert lower_navbar(ctx, nb) == lines(
        [
            '<ul class="nav-secondary">',
            '<li><a class="current" href="/b/c/">First</a></li>',
            '<li><a href="/b/d/">Second</a></li>',
            "</ul>",
        ]
    )


def test_navbar():
    nb = get_navbar_data()
    nb.set_titles({"/b/": "About", "/b/c/": "First", "/b/d/": "Second"})
    ctx = MockCtx("First", "b/c")
    assert build_navbar(ctx, nb) == lines(
        [
            '<div class="navbar">',
            '<ul class="nav-primary">',
            '<li><a href="/">󰍜</a></li>',
            '<li><a class="current" href="/b/">About</a></li>',
            "</ul>",
            '<ul class="nav-secondary">',
            '<li><a class="current" href="/b/c/">First</a></li>',
            '<li><a href="/b/d/">Second</a></li>',
            "</ul>",
            "</div>",
        ]
    )
