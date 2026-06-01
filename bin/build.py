from primitives.page_enumerate import find_meta_files

for file in find_meta_files("src"):
    # get subdir from <subdir> of <subdir>/meta.yaml
    # get root from subdir (just replace each part with ..)
    # build navbar
    # build page by page type
    # compile page
    # write into dist/<subdir>/index.html
