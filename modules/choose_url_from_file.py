from classes.PathHelper import PathHelper


def choose_url_from_file():
    pth = PathHelper()
    script_dir = pth.entry_dir

    site_url_path = script_dir / 'site_urls.txt'
    if not site_url_path.exists():
        print(f"File {site_url_path} does not exist.")
        return None
