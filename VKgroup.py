# Подключение модулей
import requests
import time
import sqlite3

# Токен и id
token = '1bdf4fb165d7cfda53459c7ab93f87dead1972c16ca0215709ac4b0b918fe44650b5e79cc101f520455fb'
group_id = 'dm'


# Основной код
def vk_download(method, parameters, token=token):
    url = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=' + token + "&v=5.21"
    response = requests.get(url)
    try:
        return (response.json())['response']
    except:
        print('Пожалуйста, обновите токен, для этого воспользуйтесь ссылкой из файла main.py')
        exit()
title_group = vk_download('groups.getById', 'group_id=' + group_id)
print(title_group)

wall = vk_download('wall.get', 'domain=' + group_id)
count_notes = wall['count']
name_group = title_group[0]['name']
n = int(input('На странице ' + str(count_notes) + ' Записей. Сколько получаем записей '))
conn = sqlite3.connect(name_group + '.db')
cur = conn.cursor()
cur.executecur.execute("""CREATE TABLE IF NOT EXISTS wall(
   number TEXT,
   author TEXT,
   comments TEXT,
   likes TEXT,
   reposts TEXT);
""")
for i in range(0, n):
    param = '&count=1&offset=' + str(i)
    note = vk_download('wall.get', 'domain=' + group_id + param)
    note = note['items'][0]
    author_note, coments_count = 'Гость', str(note['comments']['count'])
    likes_count, reposts_count = str(note['likes']['count']), str(note['reposts']['count'])
    if int(note['from_id']) == int(note['owner_id']):
        author_note = 'Владелец'
    information_recording =(i, author_note, coments_count, likes_count, reposts_count)
    cur.execute("INSERT INTO wall VALUES(?, ?, ?, ?, ?);", information_recording)
    conn.commit()
    time.sleep(0.5)
    print('Записей скачано:', i + 1)
    print('Посты скачаны. Всего скачано: ' + str(n))