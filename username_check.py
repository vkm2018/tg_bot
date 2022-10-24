import requests
from bs4 import BeautifulSoup
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}


username = input('Enter your username ')

habr = f'https://career.habr.com/{username}'
git = f'https://github.com/{username}'
tt = f'https://www.tiktok.com/@{username}'
pb = f'https://pikabu.ru/@{username}'


data_1 = []

def check_rd():
    rd = f'https://www.reddit.com/user/{username}/'
    r = requests.get(rd, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    title=soup.find('h1', class_='_3LM4tRaExed4x1wBfK1pmg')
    if title == None:
        print ('Нет такого юзера')
    else:
        data_1.append(rd)
        print('Successfully')

def check_it():
    it = f'https://www.instagram.com/{username}/'
    response = requests.get(it)
    check = 'Instagram'
    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.title.text in check:
        print ('Нет такого юзера')
    else:
        data_1.append(it)
        print ('Successfuly')

def  check_oher():
    urls = [habr, git, tt, pb]

    for i in urls:
        response = requests.get(i)
        if response.status_code == 200:
            data_1.append(i)
            print ('Successfuly')
        if response.status_code >=200:
            print ('Нет такого пользователя')

def write_json():
    pass


check_rd(), check_it(), check_oher()
print(data_1)
