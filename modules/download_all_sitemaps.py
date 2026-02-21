from urllib.parse import urlparse
from rich import print
from modules.get_site_url import get_site_url
from classes.SitemapParser import SitemapParser
from classes.HtmlDownloader import HtmlDownloader


def download_all_sitemaps(file_path: str) -> None:
    choice = input(
        "Do you want to choose a URL from the file, or to paste new one? (f/p)? ")
    site_url = get_site_url(choice, file_path)
    if not site_url:
        print("[red]No URL provided. Aborting.")
        return

    domain = urlparse(site_url).netloc
    if not domain:
        print("[red]Could not extract domain from URL. Aborting.")
        return

    print(f"[blue]Parsing sitemap: {site_url}")
    parser = SitemapParser(site_url)
    urls = parser.parse()

    if not urls:
        print("[red]No URLs found in sitemap.")
        return

    print(f"[green]Found {len(urls)} URLs. Starting download...")

    to_download = input(
        "Do you want to download all URLs? (y/n)? ")
    if to_download.lower() == 'y':
        print("[yellow]Downloading URLs...")
        # downloader = HtmlDownloader(urls, domain)
        # downloader.download_all()
    else:
        print("[yellow]Download cancelled by user.")
