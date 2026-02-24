import os
from modules.parse_indexes import parse_indexes  # оставляем как есть


def choose_html_files(root: str) -> list[str]:
    if not os.path.isdir(root):
        print(f"{root} is not a directory")
        return []

    # Собираем все .html файлы рекурсивно
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                html_files.append(full_path)

    if not html_files:
        print("Не найдено ни одного .html файла.")
        return []

    # Сортируем для предсказуемого порядка
    html_files.sort()

    # Показываем пользователю список (сокращённые имена для удобства)
    print("\nНайденные HTML-файлы:")
    display_paths = [os.path.relpath(p, root) for p in html_files]

    for i, rel_path in enumerate(display_paths):
        print(f"{i:>3}. {rel_path}")

    raw = input("\nВыберите номера (примеры: 1 | 1,3,5 | 0-4 | все): ").strip().lower()

    if raw in ("", "все", "all"):
        return sorted(html_files)

    indexes = parse_indexes(raw, len(html_files))
    if not indexes:
        print("Ничего не выбрано.")
        return []

    selected = [html_files[i] for i in indexes if 0 <= i < len(html_files)]
    return sorted(set(selected))
