from classes.Menu import Menu
from modules.check_if_is_downloads_dir import check_if_is_downloads_dir
from modules.download_all_sitemaps import download_all_sitemaps
from modules.download_by_select import download_by_select
from modules.get_site_urls_path import get_site_urls_path
from modules.show_seo import show_seo


def main():
    check_if_is_downloads_dir()
    site_urls_file_path = get_site_urls_path()

    menu_columns = ["Index", "Option"]
    menu_rows = [
        ["0", "Download all sitemap URLs"],
        ["1", "Download URLs by selecting a site URL"],
        ["2", "Show seo"],
        ["3", "Delete a record"],
        ["4", "Exit"],
    ]

    Menu.display("Main Menu", menu_columns, menu_rows)

    menu_index = Menu.choose_option()
    print(f'{menu_index}: menu_index')

    if menu_index == 0:
        download_all_sitemaps(site_urls_file_path)
    if menu_index == 1:
        download_by_select(site_urls_file_path)
    if menu_index == 2:
        show_seo()
    else:
        print("This option is not implemented yet.")


if __name__ == "__main__":
    main()
