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
    assert [x.filepath for x in nd.find("abc")] == ["abc", "abc/item"]

def test_set_title_after_add():
    nd = NavbarData("/tmp/root")

    nd.add("/tmp/root/hello/meta.yaml").title = "Hello"
    nd.add("/tmp/root/hello/hero/meta.yaml").title = "Hero"

    assert nd.find("hello")[0].title == "Hello"
    assert nd.title("hello") == "Hello"

    assert nd.title("hello", "hero") == "Hero"
