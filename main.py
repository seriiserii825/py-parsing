from classes.Menu import Menu


def main():
    menu_columns = ["Index", "Option"]
    menu_rows = [
        ["0", "View all records"],
        ["1", "Add a new record"],
        ["2", "Update an existing record"],
        ["3", "Delete a record"],
        ["4", "Exit"],
    ]

    Menu.display("Main Menu", menu_columns, menu_rows)


if __name__ == "__main__":
    main()
