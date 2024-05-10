#!/usr/bin/python3
from bs4 import BeautifulSoup
import re
with open('index.html', 'r') as file:
    src = file.read()
soup = BeautifulSoup(src, 'lxml')
title = soup.title
h3 = soup.find('h3')
h3_all = soup.find_all('h3')
user_name = soup.find('div', class_='user__name')
# print(user_name.text.strip())
user_name = soup.find('div', {'class': 'user__name', 'id': 'user-name'})
# print(user_name.text.strip())
user_info = soup.find(class_='user__info').find_all('span')
# for item in user_info:
#     print(item.text)

social__networks = soup.find(class_='social__networks').find_all('a')
for item in social__networks:
    item_text = item.text
    item_url = item.get('href')
    # print(f'{item_text}: {item_url}')

# post_text = soup.find(class_='post__text').find_parent()
post_text = soup.find(class_='post__text').find_parent('div', class_='user__post')
# print(post_text)

# find_next - find next inside tag

next_el = soup.find(class_='post__title').find_next_sibling()
# print(next_el)

# attr = link['href']
# attr = link.get('href')

# find_a_by_text = soup.find('a', string='Instagram')
find_a_by_text = soup.find('a', string=re.compile('Instagram'))
# print(find_a_by_text)

find_all_a_by_text = soup.find_all('a', string=re.compile('[Ii]nstagram'))
print(find_all_a_by_text)
