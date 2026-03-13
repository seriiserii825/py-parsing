import os
from classes.Select import Select
from classes.menu.HtmlLinksParser import HtmlLinksParser
from modules.choose_html_files import choose_html_files


def img_no_alt_role():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    di = HtmlLinksParser(html_files)
    di.parse_img_no_alt_role()
    di.show_img_no_alt_role_results()
