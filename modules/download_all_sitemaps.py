from modules.get_site_url import get_site_url


def download_all_sitemaps(file_path):
    choice = input(
        "Do you want to choose a URL from the file, or to paste new one? (f/p)? ")
    site_url = get_site_url(choice, file_path)
