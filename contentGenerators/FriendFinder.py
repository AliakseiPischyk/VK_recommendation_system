import pandas as pd
import numpy as np
import re
import vk_api


class FriendFinder:
    def __init__(self):
        vk_session = vk_api.VkApi(
            token="f1a6b8754d83592e11cb95471578587961b11f5c9f25a3f0ff070d61a9ece7e2f0078745c817dd33af67e")
        self.vk = vk_session.get_api()

    def parse_ids(self, friends):
        ids = []
        for friend in friends:
            deactivated_code = friend.get('deactivated')
            if not friend.get('is_closed') \
                    and not friend.get('blacklisted') \
                    and deactivated_code != 'banned' \
                    and deactivated_code != 'deleted':
                ids.append(friend.get('id'))
        return ids

    def getFriendsLevels(self, vk, for_user_id, depth=1, count=100):
        lvl0_friends = vk.friends.search(user_id=for_user_id,
                                         fields="blacklisted,deactivated",
                                         count=count).get('items')
        lvl0_friends_ids = self.parse_ids(lvl0_friends)

        dict_lvl_ids = {0: lvl0_friends_ids}
        for current_level in range(depth):
            current_lvl_ids = []
            for friend_id in dict_lvl_ids.get(current_level):
                next_lvl_friends = vk.friends.search(user_id=friend_id,
                                                     fields="blacklisted,deactivated",
                                                     count=count).get('items')
                for friend in next_lvl_friends:
                    deactivated_code = friend.get('deactivated')
                    print(deactivated_code)
                    if not friend.get('is_closed') \
                            and not friend.get('blacklisted') \
                            and deactivated_code != 'banned' \
                            and deactivated_code != 'deleted':
                        current_lvl_ids.append(friend.get('id'))
            dict_lvl_ids[current_level + 1] = current_lvl_ids
        return dict_lvl_ids

####################

    def get_year(self, date):
        if isinstance(date, str):
            if date.count('.') == 2:
                return re.split(r'\.', date)[2]
        return np.nan

    def is_same_city(self, row, city_id):
        if isinstance(row['city'], dict):
            return row['city'].get('id') == city_id
        return np.nan

    def get_lvl_by_id(self, user_id, dict_lvl_id):
        for key in dict_lvl_id:
            current_lvl_friend_ids = dict_lvl_id.get(key)
            if user_id in current_lvl_friend_ids:
                return key
        return np.nan

    def generate(self, for_user_id,need_common_friends,location,find_age,find_sex):
        user = self.vk.users.get(user_ids=for_user_id, fields="sex,bdate,city")[0]
        dict_lvl_ids = self.getFriendsLevels(self.vk, for_user_id=user.get('id'))

        flat_user_list = []
        for key in dict_lvl_ids:
            flat_user_list = flat_user_list + dict_lvl_ids.get(key)

        user_df = pd.DataFrame(self.vk.users.get(user_ids=flat_user_list, fields="sex,bdate,city"))

        user_df['lvl'] = user_df.apply(lambda row: self.get_lvl_by_id(row['id'], dict_lvl_ids), axis=1)
        user_df['lvl'] = pd.Series(np.interp(user_df['lvl'],
                                             (user_df['lvl'].min(),
                                              user_df['lvl'].max()),
                                             (0, 1))).sub(1).abs()

        city = 9999999 if (user.get('city') == None) else user.get('city').get('id')
        user_df['city'] = user_df.apply(lambda row: self.is_same_city(row, city), axis=1)
        user_df['city'] = user_df['city'].fillna(user_df['city'].astype(float).mean()).astype(float)

        user_df['year'] = user_df['bdate'].apply(lambda each_date: self.get_year(each_date)).astype(float)
        year = user_df['year'].mean() if (user.get('year')==None) else self.get_year(user.get('year'))
        year = user_df['year'].mean() if (year == np.nan) else year

        abs_dev = user_df['year'].sub(year).abs()
        mean_abs_dev = abs_dev.mean()
        cleared = user_df['year'].sub(year).abs().transform(lambda dev: mean_abs_dev if (dev > 50) else dev)
        cleared_scaled = pd.Series(np.interp(cleared, (cleared.min(), cleared.max()), (0, 1)))
        mean_cl_sc = cleared_scaled.mean()
        user_df['year'] = cleared_scaled.fillna(mean_cl_sc).sub(1).abs()

        user_df['sex_score'] = user_df['sex'].apply(lambda each_sex: each_sex == user.get('sex'))
        user_df['score'] = user_df['sex_score'] + user_df['year'] + user_df['city'] + user_df['lvl']
        print(user_df.shape)

        user_df = user_df.sort_values(['score'], ascending=False)
        print(user_df.shape)
        user_friends = self.vk.friends.search(user_id=user.get('id'), fields="blacklisted,deactivated", count=1000).get('items')
        user_friends_ids = self.parse_ids(user_friends)

        user_df = user_df[~user_df['id'].isin(user_friends_ids)]

        return user_df['id'].head(20).dropna().astype(int).values
