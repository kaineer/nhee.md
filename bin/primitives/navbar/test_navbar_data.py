from pathlib import Path

from primitives.navbar.data import NavbarData, NavbarItem


def test_navbar_item_parse_path_upper_lower():
    nbi = NavbarItem("foo/bar/")

    assert nbi.lower == "bar"
    assert nbi.upper == "foo"


def test_navbar_item_parse_path_upper():
    path = Path("foo/meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.upper == "foo"
    assert nbi.lower == None


def test_navbar_item_for_root():
    path = Path("meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.upper == "" or nbi.upper is None


def test_navbar_path_for_lower():
    path = Path("abc/def/meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.path == "/abc/def/"


def test_navbar_path_for_upper():
    path = Path("abc/meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.path == "/abc/"


def test_navbar_path_for_root():
    path = Path("meta.yaml").parent
    nbi = NavbarItem(str(path))

    assert nbi.path == "/"


def test_navbar_data_just_created():
    nb = NavbarData("/tmp")

    assert nb.root == "/tmp"
    assert len(nb.items) == 0


def test_navbar_data_add_root():
    nb = NavbarData("/a")
    nb.add_meta("/a/meta.yaml")

    assert len(nb.items) == 1


def test_navbar_data_add_item():
    nb = NavbarData("/a")
    nb.add_meta("/a/bcd/meta.yaml")

    assert len(nb.items) == 1


def test_navbar_data_add_same_item():
    nb = NavbarData("/a")
    ni1 = nb.add_meta("/a/bcd/e/f/meta.yaml")
    ni2 = nb.add_meta("/a/bcd/e/g/meta.yaml")

    assert len(nb.items) == 1
    assert ni1 == ni2


def test_navbar_data_add_root_and_upper():
    nb = NavbarData("/a")
    nb.add_meta("/a/meta.yaml")
    nb.add_meta("/a/bcd/meta.yaml")
    nb.add_meta("/a/bcd/e/meta.yaml")

    assert nb.upper == [None, "bcd"]


def test_find_current_root():
    nb = NavbarData("/a")
    n1 = nb.add_meta("/a/meta.yaml")
    n2 = nb.add_meta("/a/bcd/meta.yaml")

    fn = nb.find_current("/a/meta.yaml")

    assert fn == n1
    assert fn != n2


def test_find_current_upper():
    nb = NavbarData("/a")
    n1 = nb.add_meta("/a/meta.yaml")
    n2 = nb.add_meta("/a/bcd/meta.yaml")

    fn = nb.find_current("/a/bcd/meta.yaml")

    assert fn == n2
    assert fn != n1


def test_find_current_lower():
    nb = NavbarData("/a")
    n1 = nb.add_meta("/a/meta.yaml")
    n3 = nb.add_meta("/a/bcd/efg/meta.yaml")
    n4 = nb.add_meta("/a/bcd/efg/hij/meta.yaml")

    fn = nb.find_current("/a/bcd/efg/hij/meta.yaml")

    assert fn == n3
    assert n4 == n3
    assert fn != n1


def test_find_upper_for_root():
    nb = NavbarData("/a")
    nroot = nb.add_meta("/a/meta.yaml")
    n2 = nb.add_meta("/a/b/meta.yaml")

    fn = nb.find_upper("/a/meta.yaml")

    assert fn == nroot
    assert fn != n2


def test_find_upper_for_upper():
    nb = NavbarData("/a")
    n1 = nb.add_meta("/a/meta.yaml")
    n2 = nb.add_meta("/a/b/meta.yaml")
    n3 = nb.add_meta("/a/b/c/meta.yaml")

    fn = nb.find_upper("/a/b/meta.yaml")

    assert fn == n2
    assert fn != n1
    assert fn != n3


def test_find_upper_for_lower():
    nb = NavbarData("/a")
    n1 = nb.add_meta("/a/meta.yaml")
    n2 = nb.add_meta("/a/b/meta.yaml")
    n3 = nb.add_meta("/a/b/c/meta.yaml")

    fn = nb.find_upper("/a/b/c/meta.yaml")

    assert fn == n2
    assert fn != n1
    assert fn != n3


def test_find_lower_for_root():
    nb = NavbarData("/a")
    nroot = nb.add_meta("/a/meta.yaml")
    nb.add_meta("/a/b/meta.yaml")
    nb.add_meta("/a/b/c/meta.yaml")

    fn = nb.find_lower("/a/meta.yaml")

    assert fn == None
