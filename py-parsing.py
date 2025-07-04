#!/usr/bin/python3
import os

import requests
from bs4 import BeautifulSoup
from pyfzf.pyfzf import FzfPrompt
from rich.console import Console
from rich.table import Table
from termcolor import colored

from libs.select import selectMultiple

console = Console()
fzf = FzfPrompt()
if not os.path.isfile("py-parsing.py"):
    py_parsing_dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(py_parsing_dir_path)
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def getFirstPage():
    req = requests.get(domain_url + "sitemap_index.xml")
    src = req.text
    if not os.path.isfile("index.xml"):
        open("index.xml", "w")
    with open("index.xml", "w") as file:
        file.write(src)
    scrapFirstPage()


def showSitemapMenu(pages):
    choosed_columns = selectMultiple(
        ["Meta Title", "Meta Description", "Follow", "Og image"]
    )
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        row_styles=["dim", ""],
    )
    table.add_column("Page", justify="start", style="cyan")
    for column in choosed_columns:
        table.add_column(column, justify="start", style="cyan")
    print(f"Columns: {choosed_columns}")
    for page in pages:
        page_title = page.split(domain_url)[1]
        req = requests.get(page)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        table_row = []
        table_row.append(page_title)
        for column in choosed_columns:
            if column == "Meta Title":
                meta_title = soup.find("title").text
                if meta_title != "":
                    table_row.append(meta_title)
                else:
                    table_row.append(colored("No title", "red"))
            if column == "Follow":
                if soup.find("meta", attrs={"name": "robots"}):
                    meta_follow = soup.find("meta", attrs={"name": "robots"})["content"]
                    table_row.append(meta_follow)
                else:
                    table_row.append(colored("No follow", "red"))
            if column == "Meta Description":
                if soup.find("meta", attrs={"name": "description"}):
                    meta_description = soup.find("meta", attrs={"name": "description"})[
                        "content"
                    ]
                    table_row.append(meta_description)
                else:
                    table_row.append(colored("No description", "red"))
            if column == "Og image":
                if soup.find("meta", attrs={"property": "og:image"}):
                    meta_image = soup.find("meta", attrs={"property": "og:image"})[
                        "content"
                    ]
                    table_row.append(meta_image)
                else:
                    table_row.append(colored("No og image", "red"))
        table.add_row(*table_row)
    console.print(table)
    choose_another_options = input(
        colored("Do you want to choose another options? (y/n): ", "green")
    )
    if choose_another_options == "y":
        showSitemapMenu(pages)
    else:
        exit("Goodbye")


def scarpPageSitemap(file_name):
    file1 = open(file_name, "r")
    Lines = file1.readlines()
    pages = ()
    for line in Lines:
        if "<loc>" in line:
            # get text between tags
            url = line.split("<loc>")[1].split("</loc>")[0]
            print(url)
            pages = pages + (url,)
    showSitemapMenu(pages)


def scrapFirstPage():
    urls = ()
    file1 = open("index.xml", "r")
    Lines = file1.readlines()
    for line in Lines:
        if "<loc>" in line:
            url = line.split("<loc>")[1].split("</loc>")[0]
            urls = urls + (url,)
    sitemap_names = ()
    for url in urls:
        url_arr = url.split("/")
        sitemap_name = url_arr[len(url_arr) - 1]
        sitemap_names = sitemap_names + (sitemap_name,)
    sitemap_list = selectMultiple(sitemap_names)
    for sitemap in sitemap_list:
        if not os.path.isfile(sitemap):
            req = requests.get(domain_url + sitemap)
            src = req.text
            with open(sitemap, "w") as file:
                file.write(src)
            scarpPageSitemap(sitemap)


def getDomainsFromFile():
    with open("domains.txt", "r") as file:
        domains_list = ()
        domains_url_from_file = file.read()
        table = Table(
            show_header=True,
            header_style="bold magenta",
            show_lines=True,
            row_styles=["dim", ""],
        )
        table.add_column("Domain", justify="start", style="cyan")
        file1 = open("domains.txt", "r")
        Lines = file1.readlines()
        for line in Lines:
            table.add_row(line)
        console.print(table)
        for domain in domains_url_from_file.split("\n"):
            if domain != "":
                domains_list = domains_list + (domain,)
        return domains_list


def domainMenu():
    global domain_url
    domains_list = getDomainsFromFile()
    print(colored(f"1. Choose domain from list", "green"))
    print(colored(f"2. Create new domain", "blue"))
    print(colored(f"3. Remove domain", "yellow"))
    print(colored(f"4. Exit", "red"))
    choose_or_create = input("Choose option: ")
    if choose_or_create == "2":
        domain_url = input("Enter domain url: ")
        file1 = open("domains.txt", "r")
        if domain_url in file1.read():
            print(colored("Domain already exists", "red"))
            exit(colored(f"Domain {domain_url} already exists", "red"))
        if domain_url[-1] != "/":
            domain_url = domain_url + "/"
        with open("domains.txt", "a") as file:
            file.write(domain_url + "\n")
        return False
    elif choose_or_create == "1":
        domain_url = fzf.prompt(domains_list)
        domain_url = domain_url[0]
        return True
    elif choose_or_create == "3":
        domains_list = getDomainsFromFile()
        domain_url = fzf.prompt(domains_list)
        domain_url = domain_url[0]
        with open("domains.txt", "r") as file:
            lines = file.readlines()
        with open("domains.txt", "w") as file:
            for line in lines:
                if line.strip("\n") != domain_url:
                    file.write(line)
        return False
    else:
        exit("Goodbye")


def chooseDomainUrl():
    global domain_url
    if not os.path.isfile("domains.txt"):
        domain_url = input("Enter domain url: ")
        if domain_url[-1] != "/":
            domain_url = domain_url + "/"
        with open("domains.txt", "a") as file:
            file.write(domain_url + "\n")
    else:
        back = domainMenu()
        if back == False:
            return False


def mainPage():
    print(colored("Welcome to Sitemap generator", "green"))
    back = chooseDomainUrl()
    if back == False:
        mainPage()
    else:
        os.system("rm -rf *.xml")
        if not os.path.isfile("index.xml"):
            getFirstPage()
        else:
            scrapFirstPage()


if __name__ == "__main__":
    mainPage()
