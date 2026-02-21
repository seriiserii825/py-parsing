from rich import print
from classes.PathHelper import PathHelper


def check_if_is_downloads_dir():
    pth = PathHelper()
    current_dir = pth.cwd
    if current_dir.name != 'Downloads':
        print(
            '[red]Current directory is not "Downloads". '
            'Please change to the "Downloads" directory '
            'and run the program again.'
        )
        exit(1)
