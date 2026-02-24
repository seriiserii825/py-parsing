import os


def find_index_html(folder: str) -> list[str]:
    result: list[str] = []

    for root, dirs, files in os.walk(folder):
        if "index.html" in files:
            result.append(os.path.join(root, "index.html"))

    return result
