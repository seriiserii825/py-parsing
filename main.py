from classes.Menu import Menu
from modules.all_links import all_links
from modules.check_if_is_downloads_dir import check_if_is_downloads_dir
from modules.download_all_sitemaps import download_all_sitemaps
from modules.download_by_select import download_by_select
from modules.duplicate_ids import duplicate_ids
from modules.empty_links import empty_links
from modules.get_site_urls_path import get_site_urls_path
from modules.show_saved_sites_urls import show_saved_sites_urls
from modules.show_seo import show_seo
from modules.whatsap_links import whatsap_links


def main():
    check_if_is_downloads_dir()
    site_urls_file_path = get_site_urls_path()

    menu_columns = ["Index", "Option"]
    menu_items = [
        "Download all sitemap URLs",
        "Download URLs by selecting a site URL",
        "Show seo",
        "All Links",
        "Empty Links",
        "Duplicate Ids",
        "Whatsap Links",
        "Exit",
    ]

    menu_rows = [[str(i), menu_items[i]] for i in range(len(menu_items))]

    Menu.display("Main Menu", menu_columns, menu_rows)
    menu_index = Menu.choose_option()
    show_saved_sites_urls(site_urls_file_path)

    if menu_index == 0:
        download_all_sitemaps(site_urls_file_path)
    if menu_index == 1:
        download_by_select(site_urls_file_path)
    if menu_index == 2:
        show_seo()
    if menu_index == 3:
        all_links()
    if menu_index == 4:
        empty_links()
    if menu_index == 5:
        duplicate_ids()
    if menu_index == 6:
        whatsap_links()
    else:
        print("This option is not implemented yet.")


if __name__ == "__main__":
    main()
