from classes.MyTable import MyTable
from classes.SiteUrlsFile import SiteUrlsFile


def show_saved_sites_urls(file_path):
    sf = SiteUrlsFile(file_path)
    sf.load_urls()
    urls = sf.get_urls()
    mt = MyTable()
    columns = ["Index", "URL"]
    rows = [[str(i), url] for i, url in enumerate(urls)]
    mt.show("Saved Site URLs", columns, rows)
