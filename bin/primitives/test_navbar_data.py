import pytest
from navbar_data import NavbarData

def test_just_initialized():
    nd = NavbarData("/tmp/root")

    assert nd.root == "/tmp/root"
    assert nd.meta_files == []
    assert nd.upper == []

def test_adding_two_files():
    nd = NavbarData("/tmp/root")

    nd.add("/tmp/root/abc/meta.yaml")
    nd.add("/tmp/root/def/meta.yaml")
    nd.add("/tmp/root/abc/item/meta.yaml")

    assert nd.upper == ["abc", "def"]
    assert [x.menu_path for x in nd.find("abc")] == ["abc", "abc/item"]

def test_set_title_after_add():
    nd = NavbarData("/tmp/root")

    nd.add("/tmp/root/hello/meta.yaml").title = "Hello"
    nd.add("/tmp/root/hello/hero/meta.yaml").title = "Hero"

    assert nd.find("hello")[0].title == "Hello"
    assert nd.title("hello") == "Hello"

    assert nd.title("hello", "hero") == "Hero"

def test_choose_upper_level():
    nd = NavbarData("/a")

    a1 = nd.add("/a/abc/meta.yaml")
    a2 = nd.add("/a/abc/def/meta.yaml")
    a3 = nd.add("/a/abc/ghi/meta.yaml")

    chosen = nd.choose("abc")

    assert a1 == chosen

def test_choose_lower_level():
    nd = NavbarData("/a")

    a1 = nd.add("/a/abc/meta.yaml")
    a2 = nd.add("/a/abc/def/meta.yaml")
    a3 = nd.add("/a/abc/ghi/meta.yaml")

    chosen = nd.choose("abc/def")

    assert a2 == chosen

# TODO: choose current menu item by full path
# TODO: choose current upper menu item
# TODO: choose current lower menu item
def test_choose_by_full_path():
    nd = NavbarData("/a")

    a1 = nd.add("/a/abc/meta.yaml")
    a2 = nd.add("/a/abc/def/meta.yaml")
    a3 = nd.add("/a/abc/ghi/meta.yaml")

    chosen = nd.choose("abc/def/ghi/meta.yaml")

    assert a2 == chosen

