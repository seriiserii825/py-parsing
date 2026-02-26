"""Парсит все файлы и сохраняет только ссылки с href, содержащим 'whatsapp'"""

import os
from classes.Select import Select
from classes.menu.HtmlLinksParser import HtmlLinksParser
from modules.choose_html_files import choose_html_files


def whatsap_links():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    parser = HtmlLinksParser(html_files)
    parser.parse_whatsap()
    parser.show_results()
