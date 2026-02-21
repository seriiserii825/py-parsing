from classes.Menu import Menu
from modules.download_all_sitemaps import download_all_sitemaps


def main():

    menu_columns = ["Index", "Option"]
    menu_rows = [
        ["0", "Download all sitemap URLs"],
        ["1", "Add a new record"],
        ["2", "Update an existing record"],
        ["3", "Delete a record"],
        ["4", "Exit"],
    ]

    Menu.display("Main Menu", menu_columns, menu_rows)

    menu_index = Menu.choose_option()
    print(f'{menu_index}: menu_index')

    if menu_index == 0:
        download_all_sitemaps()
    else:
        print("This option is not implemented yet.")


if __name__ == "__main__":
    main()
