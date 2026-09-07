from types import SimpleNamespace

from primitives.navbar.builder import NavbarBuilder


def _ctx(subdir, web=True):
    return SimpleNamespace(subdir=subdir, web=web)


def test_context_upper_and_lower():
    builder = NavbarBuilder("src").build()
    nav = builder.context(_ctx("ai/clients"))

    titles = [item["title"] for item in nav["upper_items"]]
    assert titles == ["Home", "AI", "Dev", "Hobbies", "Blog"]

    current = [item["title"] for item in nav["upper_items"] if item["current"]]
    assert current == ["AI"]

    lower_titles = [item["title"] for item in nav["lower_items"]]
    assert lower_titles == ["Engines", "Prompts", "Web AI", "РФ"]

    current_lower = [item["title"] for item in nav["lower_items"] if item["current"]]
    assert current_lower == ["Engines"]


def test_context_urls_depend_on_web_flag():
    builder = NavbarBuilder("src").build()

    web = builder.context(_ctx("ai"))
    assert web["upper_items"][1]["url"] == "/ai/"
    assert web["lower_items"][0]["url"] == "/ai/clients/"

    local = builder.context(_ctx("ai", web=False))
    assert local["upper_items"][1]["url"] == "/ai/index.html"
    assert local["lower_items"][0]["url"] == "/ai/clients/index.html"


def test_context_home_has_no_lower():
    builder = NavbarBuilder("src").build()
    nav = builder.context(_ctx("."))

    assert nav["upper_items"][0]["current"] is True
    assert nav["lower_items"] == []
