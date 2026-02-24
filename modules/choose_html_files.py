import os

from modules.find_index_html import find_index_html
from modules.parse_indexes import parse_indexes


def choose_html_files(root: str) -> list[str]:
    if not os.path.isdir(root):
        print(f"{root} is not a directory")
        return []

    entries = sorted(os.listdir(root))

    items = [
        e for e in entries
        if os.path.isdir(os.path.join(root, e)) or e == "index.html"
    ]

    if not items:
        print("No folders or index.html found.")
        return []

    print("\nAvailable items:")
    for i, item in enumerate(items):
        mark = "📁" if os.path.isdir(os.path.join(root, item)) else "📄"
        print(f"{i:>2}. {mark} {item}")

    raw = input(
        "\nSelect by index (e.g. 1 | 1,3 | 0-4): "
    ).strip()

    indexes = parse_indexes(raw, len(items))
    if not indexes:
        print("Nothing selected.")
        return []

    result: list[str] = []

    for i in indexes:
        path = os.path.join(root, items[i])

        if os.path.isfile(path):
            # root/index.html
            result.append(path)

        else:
            # папка → ищем index.html рекурсивно
            result.extend(find_index_html(path))

    return sorted(set(result))
