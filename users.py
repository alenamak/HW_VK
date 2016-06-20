# -*- coding: utf-8 -*-

import os
import vk
import time

session = vk.Session(access_token='c3cfed00cfdc951751aca44465444db874c2ebcc6534bf2c2488329768e0db28ddd13b9969e3320fe48a6')
api = vk.API(session)

os.mkdir('C:\Users\Black\Desktop\pyth\vk')

users = api.users.search(hometown = 'Северодвинск', count = 1000)
users.remove(users[0])
uids = []
for i in users:
    uids.append(i['id'])

metadata = open('metatable.csv', 'w', encoding = 'utf-8')
metadata.write('uid' + '\t' + 'first_name' + '\t' + 'last_name' + '\t' + 'bday' + '\t' + 'langs' + '\n')

def getinfo(users):
    global metadata
    for i in uids:
        info = api.users.get(user_id=i, fields = 'sex, bdate, personal')
        uid = str(info[0]['uid'])
        first_name = info[0]['first_name']
        last_name = info[0]['last_name']
        if info[0]['sex'] == 1:
            sex = 'f'
        elif info[0]['sex'] == 2:
            sex = 'm'
        else:
            sex = ' '
        if 'bdate' in info[0]:
            bdate = info[0]['bdate']
        else:
            bdate = ' '
        if 'personal' in info[0]:
            if 'langs' in info[0]['personal']:
                if len(info[0]['personal']['langs']) == 1:
                    langs = info[0]['personal']['langs'][0]
                else:
                    langs = ', '.join(info[0]['personal']['langs'])
            else:
                langs = ' '
    metadata =  metadata + uid + '\t' + first_name + '\t' + last_name + '\t' + sex + '\t' + bdate + '\t' + langs + '\n'
    time.sleep(0.20)


def getposts(users):
    for user in users:
        texts = ''
        posts = api.wall.get(owner_id=1, filter='owner',count=100)
        posts.remove(posts[0])
        if len(posts) != 0:
            for post in posts:
                if post['post_type'] == 'post' and len(post['text']) > 1:
                    texts = texts + post['text'] + '\n'
        if len(texts) > 0:
            f = open('C:\Users\Black\Desktop\pyth\vk\\' + user + '.txt', 'w', encoding = 'utf-8')
            f.write(texts)
            f.close()


getinfo(users)
getposts(users)
metadata.close()
