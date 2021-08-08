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


#Основной код
for group_id in group_ids:
    group_info = vk_download('groups.getById', 'group_id=' + group_id)
    group_name = group_info[0]['name']
    print('Группа:', '"' + group_name + '"')
    group_info = vk_download('wall.get', 'domain=' + group_id)
    count_post = group_info['count']
    if count_post >= 50:
        n = 50
    else:
        n = count_post
    i,k = 0,0
    while i < n:
        print('# Запись №', i + 1)
        parameter_offset = '&count=1&offset=' + str(i)
        download_note = vk_download('wall.get', 'domain=' + group_id + parameter_offset)
        download_note = download_note['items'][0]
        if int(download_note['from_id']) == int(download_note['owner_id']):
            id_post = download_note['id']
            id_group = download_note['from_id']
            count_likes = download_note['likes']['count']
            if count_likes != 0:
                for j in range(0, count_likes):
                    print('Лайк', j, 'из', count_likes)
                    param_post = '&type=post&owner_id=' + str(id_group) + '&'
                    param_post += 'item_id=' + str(id_post) + '&filter=likes&'
                    param_post += 'extended=1&offset=' + str(j) + '&count=1&v=5.130'
                    post = vk_download('likes.getList', param_post)
                    post = post['items']
                    post = post[0]
                    id_page = str(post['id'])
                    spis = []
                    if not (dict_for_bd.get(id_page)):
                        page = page_download(id_page)
                        like = 1
                        spis = [page, like]
                        dict_for_bd[id_page] = spis
                    else:
                        spis = dict_for_bd[id_page]
                        spis[1] += 1
                        dict_for_bd[id_page] = spis
                    time.sleep(0.5)
                    k += 1
                    print('Записей скачано:', k)
                else:
                    n +=1
        else:
            n += 1
        i += 1
        time.sleep(0.5)
    print('Группа:', '"' + group_name + '"')
    print('Посты скачаны. Из этой группы скачано: ' + str(k))


dkeys = dict_for_bd.keys()
for dkey in dkeys:
    spis = dict_for_bd[dkey]
    id_page = spis[0][1]
    name = spis[0][0]
    phone = spis[0][2]
    site = spis[0][3]
    likes = spis[1]
    record = (id_page, name, phone, site, likes)
    cur.execute("INSERT INTO tabl VALUES(?, ?, ?, ?, ?);", record)
    conn.commit()
print('База данных готова.')







