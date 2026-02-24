import os

from classes.HtmlLinksParser import HtmlLinksParser
from classes.Select import Select
from modules.choose_html_files import choose_html_files


def all_links():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    link_parser = HtmlLinksParser(html_files)
    link_parser.parse_all()
    link_parser.show_results()
