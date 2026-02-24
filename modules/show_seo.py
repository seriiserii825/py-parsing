import os
from classes.Select import Select
from modules.choose_html_files import choose_html_files


def show_seo():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    print(f"html_files: {html_files}")
