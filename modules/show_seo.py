import os
from classes.HtmlParser import HtmlSeoParser
from classes.Select import Select
from modules.choose_html_files import choose_html_files


def show_seo():
    root_dirs = os.listdir()
    print(f"root_dirs: {root_dirs}")
    selected_dir = Select.select_with_fzf(root_dirs)
    print(f"selected_dir: {selected_dir}")
    html_files = choose_html_files(selected_dir[0])
    print(f"html_files: {html_files}")
    parser = HtmlSeoParser(html_files)
    parser.parse_all()
    parser.display()
