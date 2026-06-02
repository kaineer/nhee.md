#!/usr/bin/env python3
from pathlib import Path
import sys

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from primitives.navbar_data import build_navbar_data
from primitives.page_context import create_page_context
from primitives.page_enumerate import find_meta_files

root = str((Path(".") / "src").absolute())

meta_files = find_meta_files("src")

# Some hierarchy
navbar_data = build_navbar_data(meta_files, root)

for file in meta_files:
    context = create_page_context(root, file)
    print(context)
    # build navbar
    #   >> navbar = build_navbar(context, navbar_data)
    # build page by page type
    #   >> page = build_page(context, navbar)
    # compile page
    #   >>
    # write into dist/<subdir>/index.html
    #   >> write_page(str(page))
