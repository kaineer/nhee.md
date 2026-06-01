from pathlib import Path


def find_meta_files(src_dir="src"):
    root = Path(src_dir).absolute()
    return list(root.rglob("*/meta.yaml"))
