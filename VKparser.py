# Подключение модулей
import requests
import time
import sqlite3

# Токен и id
token = ''
group_ids = ['iqdevops']

#База данных
conn = sqlite3.connect('Pages.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tabl(
id_page TEXT,
name TEXT,
phone TEXT,
site TEXT,
likes TEXT);
""")
dict_for_bd = {}

#Функция скачивания из вк
def vk_download(method, parameters, token=token):
    url = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=' + token + "&v=5.21"
    response = requests.get(url)
    try:
        return (response.json())['response']
    except:
        print('Пожалуйста, обновите токен, для этого воспользуйтесь ссылкой из файла main.py')
        exit()

