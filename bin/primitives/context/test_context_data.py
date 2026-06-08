#
from primitives.context.data import ContextLoader

mock_files = {}
mock_content = {}

def mock_reader(path):
    if path in mock_files:
        return mock_files[path]

def mock_content_reader(path):
    if path in mock_content:
        return mock_content[path]


mock_files["/a/b/c/meta.yaml"] = {
    "page": {"type": "test", "title": "Hello, mock"},
    "links": [1, 2, 3],
}

mock_content["/a/b/c/meta.md"] = "# Header\ncontent"

context_loader = ContextLoader(root="/a", reader=mock_reader, fs_reader=mock_content_reader)


def test_load_context():
    ctx = context_loader.load("/a/b/c/meta.yaml")

    assert ctx.title == "Hello, mock"
    assert ctx.type == "test"
    assert ctx.subdir == "b/c"
    assert ctx.data["links"] == [1, 2, 3]
    assert ctx.body_content == "# Header\ncontent"
