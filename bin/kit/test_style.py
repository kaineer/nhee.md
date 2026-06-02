import pytest
from style import style

class MockCtx:
    def __init__(self, root):
        self.root = root

def test_style():
    assert (
        style("name", MockCtx("..")) == 
        "<link rel=\"stylesheet\" type=\"text/css\" href=\"../assets/name.css\">"
    )

def test_deeper_root():
    assert (
        style("name", MockCtx("../..")) == 
        "<link rel=\"stylesheet\" type=\"text/css\" href=\"../../assets/name.css\">"
    )
    
