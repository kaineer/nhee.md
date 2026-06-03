#!/usr/bin/env python3
import sys
from pathlib import Path

from primitives.context.data import ContextLoader
from primitives.navbar.data import NavbarData
from primitives.page_enumerate import find_meta_files
from widgets.navbar import build_navbar

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


root = str((Path(".") / "src").absolute())
templates_root = str((Path(".") / "src/templates"))

meta_files = find_meta_files("src")

# Some hierarchy
navbar_data = NavbarData(root)
for file in meta_files:
    navbar_data.add_meta(file)

context_loader = ContextLoader(root)

for file in meta_files:
    context = context_loader.load(file)
    # build navbar
    #   >> navbar = build_navbar(context, navbar_data)
    navbar = build_navbar(context, navbar_data)
    # build page by page type
    #   >> page = build_page(context, navbar)
    # compile page
    #   >>
    # write into dist/<subdir>/index.html
    #   >> write_page(str(page))
