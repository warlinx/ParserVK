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



#Функция для получения информации со страницы пользователя
def page_download(page_id):
    page_id = str(page_id)
    parameters_for_download = '&fields=photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, ' \
                              'photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, ' \
                              'online, domain, has_mobile, contacts, site, education, universities, schools, status, ' \
                              'last_seen, followers_count, common_count, occupation, nickname, relatives, relation, ' \
                              'personal, connections, exports, activities, interests, music, movies, tv, books, ' \
                              'games, about, quotes, can_post, can_see_all_posts, can_see_audio, ' \
                              'can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, ' \
                              'timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, ' \
                              'military, blacklisted, blacklisted_by_me, can_be_invited_group '
    page_info = vk_download('users.get','users_ids=' + page_id + parameters_for_download)
    page_info = page_info[0]
    page_name = page_info['first_name'] + ' ' + page_info['last_name']
    try:
        mobile_phone = page_info['mobile_phone']
        if mobile_phone == '':
            mobile_phone = 'None'
    except:
        mobile_phone = 'None'
    try:
        site = page_info['site']
        if site == '':
            site = 'None'
    except:
        site = 'None'
    information_from_page = inform = [page_name, page_id, mobile_phone, site]
    time.sleep(0.5)
    return information_from_page





