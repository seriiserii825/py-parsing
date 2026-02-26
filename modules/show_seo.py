import os
from classes.menu.HtmlSeoParser import HtmlSeoParser
from classes.Select import Select
from modules.choose_html_files import choose_html_files


def show_seo():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    parser = HtmlSeoParser(html_files)
    parser.parse_all()
    parser.display()
