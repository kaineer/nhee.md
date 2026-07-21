from primitives.meta import Meta

def test_works_like_object():
    m = Meta({ "key": "value" })
    assert m.key == "value"

def test_returns_is_none_when_no_key_is_present():
    m = Meta()
    assert m.key == None
    assert m.foo.bar == None

def test_works_with_nested_dict():
    m = Meta({ "key": { "nested": "value" }})
    assert m.key.nested == "value"
