from primitives.template.template import Template


def test_simple_template():
    t = Template("before %root% is replaced")
    t1 = t.apply({"root": "home"})

    assert t1.text == "before home is replaced"


def test_replace_twice():
    t = Template("target is %root%")
    t1 = t.apply({"root": "get %target%", "target": "stronger"})
    t2 = t.apply({"root": "get %target%"}).apply({"target": "stronger"})

    assert t1.text == "target is get stronger"
    assert t2.text == "target is get stronger"
