# подключение модулей
import requests
import time

# токен и id
token = '97ad13079762c39ef7b88bc38b2b90735f4c98bb99cdae1249ee2ba70440b7438a148b828c24d92de0c3b'
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
n = int(input('На странице ' + str(count_notes) + ' записей. Сколько скачаем записей? '))
for i in range(0, n):
    param = '&count=1&offset=' + str(i)
    note = vk_download('wall.get', 'owner_id=' + new_id + param)
    note = note['items'][0]
    author_note, coments_count = 'Гость', str(note['comments']['count'])
    likes_count, reposts_count = str(note['likes']['count']), str(note['reposts']['count'])
    if int(note['from_id']) == int(note['owner_id']):
        author_note = 'Владелец'
    print(author_note, coments_count, likes_count, reposts_count)
