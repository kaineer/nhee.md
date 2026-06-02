import pytest
from tag import tag

def test_empty_tag():
    assert tag("li") == "<li></li>"

def test_tag_with_child():
    assert tag("b", children="text") == "<b>text</b>"

def test_tag_with_none_in_list():
    assert tag("b", children=[
        "hello", None
    ]) == "<b>hello</b>"

def test_tag_with_children_list():
    assert tag("b", children=[
        tag("span", children="first"),
        tag("span", children="second")
    ]) == "<b><span>first</span><span>second</span></b>"

def test_tag_with_attribute():
    assert tag("a", 
               attr={"href": "http://127.0.0.1"}, 
               children="localhost"
    ) == "<a href=\"http://127.0.0.1\">localhost</a>"

def test_tag_with_classname():
    assert tag("div", classname="cell", children="abc") == (
            "<div class=\"cell\">abc</div>"
    )

def test_tag_empty_by_default():
    assert tag("hr") == "<hr>"
