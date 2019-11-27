import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from numpy.random import randint


class ChatBot:
    class UserInfo:
        INIT_STATE = 0
        AGE_INPUT_STATE = 1
        SEX_INPUT_STATE = 2
        LOCATION_INPUT_STATE = 3
        NEED_COMMON_FRIENDS_INPUT_STATE = 4

        def __init__(self):
            self.need_common_friends = True
            self.location = "Минск"
            self.find_sex = 2
            self.find_age = 18
            self.state = self.INIT_STATE
            self.ready = False

    def __init__(self):
        vk_session = vk.VkApi(
            token="154e00683e8ab940c179f50c4f04a4ebfd9da709bcdd355e002a88095aac0a80cf26312d1c016acf3697d")
        self.keyboard = open("bot/KB.json", "r").read()
        self.longPoll = VkLongPoll(vk_session)
        self.vk_ = vk_session.get_api()
        self.users = {}

    def make_links(self, array_of_ids):
        ret = []
        for each_id in array_of_ids:
            new_link = f"https://vk.com/id{each_id}"
            ret.append(new_link)
        return ret

    def run(self, generator):
        d_id_info = {}
        for event in self.longPoll.listen():
            if event.type == VkEventType.MESSAGE_NEW \
                    and event.to_me \
                    and event.text \
                    and event.from_user:
                if self.users.get(event.user_id) is None:
                    self.users[event.user_id] = self.UserInfo()
                    self.vk_.messages.send(
                        user_id=event.user_id,
                        message=":)",
                        random_id=randint(dtype="int64", low=0, high=0xffffffff),
                        keyboard=self.keyboard
                    )
                    continue
                if hasattr(event, "payload"):
                    if event.text == "Ввести данные":
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message="Введите свой возраст",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff)
                        )
                        self.users[event.user_id].state = self.UserInfo.AGE_INPUT_STATE
                    elif event.text == "Запустить":
                        if self.users[event.user_id].ready:
                            self.vk_.messages.send(
                                user_id=event.user_id,
                                message='\n'.join(self.make_links(
                                    generator.generate(event.user_id,
                                                       self.users[event.user_id].need_common_friends,
                                                       self.users[event.user_id].location,
                                                       self.users[event.user_id].find_age,
                                                       self.users[event.user_id].find_sex))),
                                random_id=randint(dtype="int64", low=0, high=0xffffffff)
                            )
                            self.vk_.messages.send(
                                user_id=event.user_id,
                                message="Here are recommendations for you",
                                random_id=randint(dtype="int64", low=0, high=0xffffffff)
                            )
                        else:
                            self.vk_.messages.send(
                                user_id=event.user_id,
                                message="Сначала введите данные",
                                random_id=randint(dtype="int64", low=0, high=0xffffffff),
                                keyboard = self.keyboard
                            )
                else:
                    if self.users[event.user_id].state == self.UserInfo.AGE_INPUT_STATE:
                        self.users[event.user_id].age = int(event.text)
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message="Введите sex",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff),
                        )
                        self.users[event.user_id].state = self.UserInfo.SEX_INPUT_STATE
                    elif self.users[event.user_id].state == self.UserInfo.SEX_INPUT_STATE:
                        self.users[event.user_id].sex = int(event.text)
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message="Введите location",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff),
                        )
                        self.users[event.user_id].state = self.UserInfo.LOCATION_INPUT_STATE
                    elif self.users[event.user_id].state == self.UserInfo.LOCATION_INPUT_STATE:
                        self.users[event.user_id].location = event.text
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message="Введите NEED COMMON FRIENDS",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff),
                        )
                        self.users[event.user_id].state = self.UserInfo.NEED_COMMON_FRIENDS_INPUT_STATE
                    elif self.users[event.user_id].state == self.UserInfo.NEED_COMMON_FRIENDS_INPUT_STATE:
                        if "Yes" in event.text:
                            self.users[event.user_id].need_common_friends = True
                        else:
                            self.users[event.user_id].need_common_friends = False
                        self.users[event.user_id].ready = True
                        self.users[event.user_id] = self.UserInfo
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message=":)",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff),
                            keyboard=self.keyboard
                        )
                        self.users[event.user_id].state = self.UserInfo.INIT_STATE
                    else:
                        self.users[event.user_id] = self.UserInfo
                        self.vk_.messages.send(
                            user_id=event.user_id,
                            message=":)",
                            random_id=randint(dtype="int64", low=0, high=0xffffffff),
                            keyboard=self.keyboard
                        )


