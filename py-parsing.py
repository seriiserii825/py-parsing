#!/usr/bin/python3
import requests
import csv
import os
import json
import xml.etree.ElementTree as ET
from tabulate import tabulate
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from rich.console import Console
from rich.table import Table
from termcolor import colored
console = Console()


domain_url = input('Enter domain url: ')

if domain_url == '':
    exit('You did not enter a domain url')

headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

def getFirstPage():
    req = requests.get(domain_url + 'sitemap_index.xml')
    src = req.text
    if not os.path.isfile('index.xml'):
        touch = open('index.xml', 'w')
    with open('index.xml', 'w') as file:
        file.write(src)
    scrapFirstPage()

def scarpPageSitemap():
    urls = ()
    file1 = open('page-sitemap.xml', 'r')
    Lines = file1.readlines()
    pages = ()
    for line in Lines:
        if '<loc>' in line:
            # get text between tags
            url = line.split('<loc>')[1].split('</loc>')[0]
            pages = pages + (url,)

    table = Table(show_header=True, header_style="bold magenta", show_lines=True, row_styles=["dim", ""])
    table.add_column("Page", justify="start", style="cyan")
    table.add_column("Meta Title", justify="start", style="green")
    table.add_column("Meta Description", justify="start")
    for page in pages:
        print(f'Getting {page}')
        # page_title = 'title'
        page_title = page.split(domain_url)[1]
        print(colored(f'Getting {page_title}', "green"))
        req = requests.get(page)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        #get meta title
        result_title = ''
        result_description = ''
        meta_title = soup.find('title').text
        if meta_title == '':
            result_title = colored('No meta title', 'red')
        else:
            result_title = meta_title
        if soup.find('meta', attrs={'name': 'description'}):
            meta_description = soup.find('meta', attrs={'name': 'description'})['content']
            result_description = meta_description
        else: 
            result_description = colored('No meta description', 'red')
        table.add_row(
            page_title,
            result_title,
            result_description
        )
    console.print(table)

def scrapFirstPage():
    urls = ()
    file1 = open('index.xml', 'r')
    Lines = file1.readlines()
    for line in Lines:
        if '<loc>' in line:
            # get text between tags
            url = line.split('<loc>')[1].split('</loc>')[0]
            urls = urls + (url,)
        
    for url in urls:
        if 'page-sitemap' in url:
            if not os.path.isfile('page-sitemap.xml'):
                touch = open('page-sitemap.xml', 'w')
                req = requests.get(domain_url + 'page-sitemap.xml')
                src = req.text
                with open('page-sitemap.xml', 'w') as file:
                    file.write(src)
                scarpPageSitemap()
            else:
                scarpPageSitemap()

def mainPage():
    clear_all = input('Do you want to clear all files? (y/n): ')
    if clear_all == 'y':
        if os.path.isfile('index.xml'):
            os.remove('index.xml')
        if os.path.isfile('page-sitemap.xml'):
            os.remove('page-sitemap.xml')
    if not os.path.isfile('index.xml'):
        getFirstPage()
    else:
        scrapFirstPage()

if __name__ == '__main__':
    mainPage()
