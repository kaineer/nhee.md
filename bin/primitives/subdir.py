#
root_path = "/"


def subdir(path, count=None):
    if path is None:
        return root_path
    if path == ".":
        return root_path
    if path == "":
        return root_path

    if count is None:
        return f"/{path}/"
    parts = path.split("/")[0:count]
    path = "/".join(parts)
    return f"/{path}/"
