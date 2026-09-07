from types import SimpleNamespace

from primitives.breadcrumbs.builder import BreadcrumbsBuilder


def _ctx(subdir, web=True):
    return SimpleNamespace(subdir=subdir, web=web)


def _slugs(level):
    return [item["slug"] for item in level]


def _flags(level, key):
    return [item["slug"] for item in level if item[key]]


def test_nav_page_has_no_crumbs():
    crumbs = BreadcrumbsBuilder("src").build().context(_ctx("hobby/nihon"))
    assert crumbs["crumb_levels"] == []


def test_home_has_no_crumbs():
    crumbs = BreadcrumbsBuilder("src").build().context(_ctx("."))
    assert crumbs["crumb_levels"] == []


def test_off_nav_section_lists_siblings_under_navbar():
    crumbs = BreadcrumbsBuilder("src").build().context(_ctx("hobby/shed"))
    levels = crumbs["crumb_levels"]
    assert len(levels) == 1

    slugs = _slugs(levels[0])
    assert slugs[:5] == ["Manga", "Anime", "Games", "日本語", "Tools"]
    assert slugs[-1] == "Shed prompts"
    assert _flags(levels[0], "current") == ["Shed prompts"]
    assert _flags(levels[0], "next") == []


def test_off_nav_leaf_has_section_and_page_levels():
    crumbs = BreadcrumbsBuilder("src").build().context(_ctx("hobby/shed/01"))
    levels = crumbs["crumb_levels"]
    assert len(levels) == 2
    assert _flags(levels[0], "current") == ["Shed prompts"]
    assert _flags(levels[1], "current") == ["Plump chubby in skirt"]
    assert _flags(levels[1], "next") == []


def test_below_navbar_skips_directories_without_pages():
    crumbs = BreadcrumbsBuilder("src").build().context(
        _ctx("hobby/nihon/kanji/n5/01")
    )
    levels = crumbs["crumb_levels"]
    assert len(levels) == 2

    assert _slugs(levels[0]) == ["漢字 N4", "漢字 N5"]
    assert _flags(levels[0], "current") == ["漢字 N5"]
    assert _flags(levels[0], "next") == []

    assert _flags(levels[1], "current") == ["Числа от 1 до 10"]
    assert _flags(levels[1], "next") == ["Природа и стихии"]
    assert levels[1][0]["url"] == "/hobby/nihon/kanji/n5/01/"


def test_prompts_leaf_is_one_level_below_navbar():
    crumbs = BreadcrumbsBuilder("src").build().context(_ctx("ai/prompts/caveman"))
    levels = crumbs["crumb_levels"]
    assert len(levels) == 1
    assert _slugs(levels[0]) == ["Caveman prompt"]
    assert _flags(levels[0], "current") == ["Caveman prompt"]
    assert _flags(levels[0], "next") == []


def test_urls_depend_on_web_flag():
    builder = BreadcrumbsBuilder("src").build()

    web = builder.context(_ctx("hobby/shed"))
    assert web["crumb_levels"][0][-1]["url"] == "/hobby/shed/"

    local = builder.context(_ctx("hobby/shed", web=False))
    assert local["crumb_levels"][0][-1]["url"] == "/hobby/shed/index.html"
