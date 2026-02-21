from rich import print
from classes.Select import Select
from classes.SiteUrlsFile import SiteUrlsFile


def get_site_url(choice, file_path):
    sf = SiteUrlsFile(file_path)
    site_url = ''
    if choice.lower() == 'f':
        sf.load_urls()
        urls = sf.get_urls()
        print(f'{urls}: urls')
        selected_urls = Select.select_with_fzf(urls)
        if selected_urls:
            site_url = selected_urls[0].strip()
        else:
            print("[red]No URL selected.")
            exit(1)
    else:
        site_url = input("Please paste the URL of the sitemap: ")
        if site_url and site_url.endswith('.xml'):
            sf.add_url(site_url)
            print(f'[green]{site_url}: site_url')
            site_url = site_url.strip()
        else:
            print("[red]Invalid URL. Please make sure it ends with '.xml'.")
            exit(1)

    return site_url
