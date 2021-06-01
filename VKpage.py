# подключение модулей
import requests
import time
import sqlite3

# токен и id
token = 'token'
page_id = 'dm'


# основной код
def vk_download(method, parameters, token=token):
    url = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=' + token + "&v=5.21"
    response = requests.get(url)
    try:
        return (response.json())['response']
    except:
        print('Пожалуйста обновите токен, для этого воспользуйтесь ссылкой из файла main.py')
        exit()


title_page = vk_download('users.get', 'user_ids=' + page_id)
print(title_page)

new_id = str(title_page[0]['id'])
wall = vk_download('wall.get', 'owner_id=' + new_id)
count_notes = wall['count']
name_page = title_page[0]['first_name'] + ' ' + title_page[0]['last_name']
n = int(input('На странице ' + str(count_notes) + ' записей. Сколько скачаем записей? '))
conn = sqlite3.connect(name_page+'.db')
for i in range(0, n):
    param = '&count=1&offset=' + str(i)
    note = vk_download('wall.get', 'owner_id=' + new_id + param)
    note = note['items'][0]
    author_note, coments_count = 'Гость', str(note['comments']['count'])
    likes_count, reposts_count = str(note['likes']['count']), str(note['reposts']['count'])
    if int(note['from_id']) == int(note['owner_id']):
        author_note = 'Владелец'
    print(author_note, coments_count, likes_count, reposts_count)
