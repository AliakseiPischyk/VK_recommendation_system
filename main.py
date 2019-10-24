import pandas as pd
import numpy as np
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import random

import vk_api as vk

vk_session = vk.VkApi(token=some_token)
vk = vk_session.get_api()

basic_friends = vk.friends.search(user_id=some_id,fields="blacklisted,deactivated", count=100)
friens = basic_friends.get('items')
fr_id = []
for f in friens:
    a = f.get('deactivated')
    if not f.get('is_closed') and not f.get('blacklisted') and a != 'banned' and a != 'deleted':
        fr_id.append(f.get('id'))
lvlAndIds = {0:fr_id}

skok = 2
level = 0
for level in range(skok):
    mini_fr_id = []
    for friend in lvlAndIds.get(level):
        vals = vk.friends.search(user_id=friend,fields="blacklisted,deactivated", count=100).get('items')
        for f in vals:
            a = f.get('deactivated')
            if not f.get('is_closed') and not f.get('blacklisted') and a != 'banned' and a != 'deleted':
                mini_fr_id.append(f.get('id'))
    lvlAndIds[level + 1] = mini_fr_id
    level = level + 1
