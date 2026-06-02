from pathlib import Path

from primitives.navbar.data import NavbarItem


def test_navbar_item_parse_path_upper_lower():
    nbi = NavbarItem("foo/bar/")

    assert nbi.lower == "bar"
    assert nbi.upper == "foo"


def test_navbar_item_parse_path_upper():
    path = Path("foo/meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.upper == "foo"
    assert nbi.lower == None
