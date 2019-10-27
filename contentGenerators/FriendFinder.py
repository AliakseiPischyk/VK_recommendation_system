import pandas as pd

class FriendFinder:
    def getFriendsLevels(self, vk, for_user_id, depth=1, count=100):
        lvl0Friends = vk.friends.search(user_id=for_user_id, fields="blacklisted,deactivated", count=count).get('items')
        lvl0_friends_ids=[]
        for friend in lvl0Friends:
            deactivated_code = friend.get('deactivated')
            if not friend.get('is_closed') and not friend.get('blacklisted') and deactivated_code != 'banned' and deactivated_code != 'deleted':
                lvl0_friends_ids.append(friend.get('id'))
        dict_lvl_ids = {0: lvl0_friends_ids}

        for current_level in range(depth):
            current_lvl_ids = []
            for friend_id in dict_lvl_ids.get(current_level):
                next_lvl_friends = vk.friends.search(user_id=friend_id, fields="blacklisted,deactivated", count=count).get('items')
                for friend in next_lvl_friends:
                    deactivated_code = friend.get('deactivated')
                    if not friend.get('is_closed') and not friend.get('blacklisted') and deactivated_code != 'banned' and deactivated_code != 'deleted':
                        current_lvl_ids.append(friend.get('id'))
            dict_lvl_ids[current_level + 1] = current_lvl_ids

####################

    def get_lvl_by_id(self, user_id, dict_lvl_id):
        for key in dict_lvl_id:
            current_lvl_friend_ids = dict_lvl_id.get(key)
            if user_id in current_lvl_friend_ids:
                return key
        return pd.nan

    def generate(self, user, parameters):
        # some ML magic gonna be here
        return 'friend1Link, friend2link...'
