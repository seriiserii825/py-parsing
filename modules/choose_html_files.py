import os
from modules.parse_indexes import parse_indexes  # keep as is


def choose_html_files(root: str) -> list[str]:
    if not os.path.isdir(root):
        print(f"{root} is not a directory")
        return []

    # Collect all .html files recursively
    html_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                html_files.append(full_path)

    if not html_files:
        print("No .html files were found.")
        return []

    # Sort for predictable order
    html_files.sort()

    # Show the list to the user (shortened paths for convenience)
    print("\nFound HTML files:")
    display_paths = [os.path.relpath(p, root) for p in html_files]

    for i, rel_path in enumerate(display_paths):
        print(f"{i:>3}. {rel_path}")

    raw = input("\nSelect numbers (examples: 1 | 1,3,5 | 0-4 | all): ").strip().lower()

    if raw in ("", "all"):
        return sorted(html_files)

    indexes = parse_indexes(raw, len(html_files))
    if not indexes:
        print("Nothing selected.")
        return []

    selected = [html_files[i] for i in indexes if 0 <= i < len(html_files)]
    return sorted(set(selected))
