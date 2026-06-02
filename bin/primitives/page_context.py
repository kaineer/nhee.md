from dataclasses import dataclass
from pathlib import Path

import yaml

__all__ = ["create_page_context"]


def path_to_root(root_path: str, path: str) -> str:
    """Упрощённая версия с pathlib."""
    root = Path(root_path).resolve()
    current_file = Path(path).resolve()
    current_dir = current_file.parent

    # Вычисляем, сколько шагов нужно сделать вверх
    try:
        # Путь от current_dir до root
        relative = root.relative_to(current_dir)
        return str(relative)
    except ValueError:
        # Если root не является поддиректорией current_dir,
        # считаем количество parent шагов
        depth = len(current_dir.relative_to(root).parents)
        return "/".join([".."] * depth) if depth > 0 else "."


def path_from_root(root_path: str, path: str) -> str:
    """Упрощённая версия."""
    root = Path(root_path).resolve()
    current_dir = Path(path).resolve().parent
    return str(current_dir.relative_to(root))


@dataclass
class PageContext:
    metafile: str
    root: str  # project root
    subdir: str  # current page subdir
    type: str  # page type
    title: str  # page title


def create_page_context(root_path: str, path: str) -> PageContext:
    """
    Создает PageContext на основе meta.yaml файла.

    Args:
        root_path: абсолютный путь к корневому каталогу проекта
        path: путь к файлу meta.yaml

    Returns:
        PageContext объект с заполненными полями
    """
    root = Path(root_path).resolve()
    meta_file = Path(path).resolve()

    # Читаем meta.yaml
    with open(meta_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Извлекаем page.type и page.title
    page_data = data.get("page", {})
    page_type = page_data.get("type", "default")
    page_title = page_data.get("title", "Untitled")

    # Вычисляем subdir (путь от корня до директории с meta.yaml)
    meta_dir = meta_file.parent
    subdir = str(meta_dir.relative_to(root))

    # Если subdir = '.' (файл в корне), делаем пустую строку
    if subdir == ".":
        subdir = ""

    return PageContext(
        metafile=str(meta_file),
        root=path_to_root(str(root), str(meta_file)),
        subdir=subdir,
        type=page_type,
        title=page_title,
    )
