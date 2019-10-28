import pandas as pd
import numpy as np
import vk_api as vk
from bot import chatbot
from bot.chatbot import ChatBot
from contentGenerators import FriendFinder
import re
from sklearn import preprocessing

def get_year(date):
    if isinstance(date, str):
        if date.count('.') == 2:
            return re.split(r'\.', date)[2]
    return np.nan

def is_same_city(row, city_id):
    if isinstance(row['city'], dict):
        return row['city'].get('id') == city_id
    return np.nan


def get_lvl_by_id(user_id, dict_lvl_id):
    for key in dict_lvl_id:
        current_lvl_friend_ids = dict_lvl_id.get(key)
        if user_id in current_lvl_friend_ids:
            return key
    return np.nan

vk_session = vk.VkApi(token=...)
vk = vk_session.get_api()

basic_friends = vk.friends.search(user_id=..., fields="blacklisted,deactivated", count=10)
friens = basic_friends.get('items')
fr_id = []
for f in friens:
    a = f.get('deactivated')
    if not f.get('is_closed') and not f.get('blacklisted') and a != 'banned' and a != 'deleted':
        fr_id.append(f.get('id'))
lvlAndIds = {0: fr_id}

skok = 2
level = 0
for level in range(skok):
    mini_fr_id = []
    for friend in lvlAndIds.get(level):
        vals = vk.friends.search(user_id=friend, fields="blacklisted,deactivated", count=10).get('items')
        for f in vals:
            a = f.get('deactivated')
            if not f.get('is_closed') and not f.get('blacklisted') and a != 'banned' and a != 'deleted':
                mini_fr_id.append(f.get('id'))
    lvlAndIds[level + 1] = mini_fr_id
    level = level + 1

flatUserList = []
for key in lvlAndIds:
    flatUserList = flatUserList + lvlAndIds.get(key)

kek = pd.DataFrame(vk.users.get(user_ids=flatUserList, fields="sex,bdate,city,common_count"))

kek['lvl'] = kek.apply(lambda row: get_lvl_by_id(row['id'], lvlAndIds), axis=1)
kek['is_same_city'] = kek.apply(lambda row: is_same_city(row, 282), axis=1)
kek['is_same_city'] = kek['is_same_city'].fillna(kek['is_same_city'].astype(float).mean())

kek['year'] = kek['bdate'].apply(lambda each_date: get_year(each_date)).astype(int)
abs_dev = kek['year'].sub(2000).abs()
mean_abs_dev = abs_dev.mean()
cleared = kek['year'].sub(2000).abs().transform(lambda dev: mean_abs_dev if (dev > 50) else dev)
cleared_scaled = pd.Series(np.interp(cleared, (cleared.min(), cleared.max()), (0, 1)))
mean_cl_sc = cleared_scaled.mean()
weigts_age = cleared_scaled.fillna(mean_cl_sc).sub(1).abs()

