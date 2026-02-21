from classes.PathHelper import PathHelper


def get_site_urls_path():
    ph = PathHelper()
    return f"{ph.entry_dir}/sitemap_urls.txt"
