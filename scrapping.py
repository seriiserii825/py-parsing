#!/usr/bin/python3
import requests
import csv
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

def handleCategoryPage(all_categories_dict):
    iteration_count = int(len(all_categories_dict)) - 1
    print(f"Iteration count: {iteration_count}")
    count = 0
    for category_title, category_link in all_categories_dict.items():
        print(f'iteration {count} of {iteration_count}')
        req = requests.get(category_link, headers=headers)
        src = req.text
        with open(f'html/{count}_{category_title}.html', 'w') as file:
            file.write(src)
        with open(f'html/{count}_{category_title}.html') as file:
            src = file.read()
            soup = BeautifulSoup(src, 'lxml')

            alert_block = soup.find(class_='uk-alert-danger')
            if alert_block is not None:
                continue

            all_th = soup.find(class_='mzr-tc-group-table').find('thead').find_all('th')
            product = all_th[0].text
            calories = all_th[1].text
            proteins = all_th[2].text
            fats = all_th[3].text
            carbohydrates = all_th[4].text
            if not os.path.isdir('csv'):
                os.mkdir('csv')
            with open(f'csv/{count}_{category_title}.csv', 'w', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
        products_tr = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        for item in products_tr:
            products_tds = item.find_all('td')
            title = products_tds[0].find('a').text
            calories = products_tds[1].text
            proteins = products_tds[2].text
            fats = products_tds[3].text
            carbohydrates = products_tds[4].text
            with open(f'csv/{count}_{category_title}.csv', 'a', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )

        count += 1
        iteration_count -= 1
        if iteration_count == 0:
            print('Scrapping is done')
            break

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
    handleCategoryPage(all_categories_dict)

def mainPage():
    if not os.path.isdir('html'):
        os.mkdir('html')
        getFirstPage()
    else:
        scrapFirstPage()

if __name__ == '__main__':
    mainPage()
