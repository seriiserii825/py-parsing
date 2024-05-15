#!/usr/bin/python3
import requests
import os
import json
from bs4 import BeautifulSoup

domain_url = 'https://health-diet.ru'
url = domain_url + '/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

def getFirstPage():
    req = requests.get(url)
    src = req.text

    with open('html/index.html', 'w') as file:
        file.write(src)

def saveToJson(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def scrapFirstPage():
    src = open('html/index.html').read()
    soup = BeautifulSoup(src, 'lxml')
    categories_links = soup.find_all(class_='mzr-tc-group-item-href')
    all_categories_dict = {}
    for item in categories_links:
        symbols = [' ', ',', '(', ')', '/', '-']
        title = item.text
        link = domain_url + item.get('href')
        for s in symbols:
            if s in title:
                title = title.replace(s, '_')
                title = title.rstrip('_')
        all_categories_dict[title] = link
        if not os.path.isdir('json'):
            os.mkdir('json')
        saveToJson('json/all_categories_dict.json', all_categories_dict)

def mainPage():
    if not os.path.isdir('html'):
        os.mkdir('html')
        getFirstPage()
    else:
        scrapFirstPage()

if __name__ == '__main__':
    mainPage()
