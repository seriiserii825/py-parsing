import os
from classes.Select import Select
from classes.menu.DuplicateIdsParser import DuplicateIdsParser
from modules.choose_html_files import choose_html_files


def duplicate_ids():
    root_dirs = os.listdir()
    selected_dir = Select.select_with_fzf(root_dirs)
    html_files = choose_html_files(selected_dir[0])
    di = DuplicateIdsParser(html_files)
    di.parse_all()
    di.display()
