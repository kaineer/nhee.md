from primitives.navbar.data import NavbarData
from widgets.navbar import navbar_item, upper_navbar


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
            '<div class="nav-primary">',
            '<li><a class="current" href="/">󰍜</a></li>',
            '<li><a href="/b/">About</a></li>',
            "</div>",
        ]
    )


def test_upper_navbar_about():
    nb = get_navbar_data()
    nb.set_titles({"/b/": "About"})
    ctx = MockCtx("About", "b")

    assert upper_navbar(ctx, nb) == lines(
        [
            '<div class="nav-primary">',
            '<li><a href="/">󰍜</a></li>',
            '<li><a class="current" href="/b/">About</a></li>',
            "</div>",
        ]
    )


# TODO: test_lower_navbar
# TODO: test_navbar
