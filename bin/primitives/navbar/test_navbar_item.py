from bin.primitives.navbar.data import NavbarItem


def test_navbar_item_root():
    ni = NavbarItem({"title": "Home", "url": ""})

    assert ni.title == "Home"
    assert ni.url == "/"

    assert ni.upper == None


def test_navbar_item_upper():
    ni = NavbarItem({"title": "AI", "url": "ai"})

    assert ni.title == "AI"
    assert ni.url == "/ai/"

    assert ni.upper == "ai"
    assert ni.lower == None


def test_navbar_item_with_parent():
    pi = NavbarItem({"title": "AI", "url": "ai"})
    ni = NavbarItem({"title": "Engines", "url": "clients"}, pi)

    assert ni.title == "Engines"
    assert ni.url == "/ai/clients/"
    assert ni.upper == "ai"
    assert ni.lower == "clients"


# def test_navbar_item_with_grandparent():
#     gi = NavbarItem({"title": "AI", "url": "ai"})
#     pi = NavbarItem({"title": "Prompts", "url": "prompts"}, gi)
#     ni = NavbarItem({"title": "Caveman", "url": "caveman"}, pi)
#
#     assert ni.title == "Caveman"
#     assert ni.upper == "ai"
#     assert ni.lower == "prompts"
#     assert ni.url == "/ai/prompts/caveman/"
