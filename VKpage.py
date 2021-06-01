# подключение модулей
import requests
import time

# токен и id
token = 'f9cb1213f9cb1213f9cb1213e3f9b300ddff9cbf9cb1213997d365f6f6769cf12d0718'
page_id = 'dm'
n = 1


# основной код
def vk_download(method, parameters, token=token):
    url = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=' + token + "&v=5.21"
    response = requests.get(url)
    return (response.json())


title_page = vk_download('users.get', 'user_ids=' + page_id)
title_page = title_page['response']
new_id = str(title_page[0]['id'])
wall = vk_download('wall.get', 'owner_id=' + new_id)
wall = wall['response']
print(wall['count'])
print(len(wall['items']))

for i in range(0, n):
    param = '&count=1&offset=' + str(i)
    note = vk_download('wall.get', 'owner_id=' + new_id + param)
