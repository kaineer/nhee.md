from primitives.subdir import subdir


def test_subdir_of_root():
    assert subdir("") == "/"
    assert subdir(".") == "/"
    assert subdir(None) == "/"


def test_subdir_of_upper():
    assert subdir("hello") == "/hello/"


def test_subdir_of_lower():
    assert subdir("hello/there") == "/hello/there/"


def test_subdir_of_too_deep():
    assert subdir("hello/there", 1) == "/hello/"
    assert subdir("hello/there/again", 2) == "/hello/there/"
