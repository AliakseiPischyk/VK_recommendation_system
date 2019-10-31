import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from numpy.random import randint


class ChatBot:
    def __init__(self):
        vk_session = vk.VkApi(
            token="8696663cd551138e2d8a6526513dae3e3397b01f939d260d7b389ae057f2b7aa5b476f88f3584d4722474")
        self.longPoll = VkLongPoll(vk_session)
        self.vk_ = vk_session.get_api()

    def make_links(self, array_of_ids):
        ret = []
        for each_id in array_of_ids:
            new_link = "https://vk.com/id"+str(each_id)
            ret.append(new_link)
        return ret

    def run(self, generator):
        for event in self.longPoll.listen():
            if event.type == VkEventType.MESSAGE_NEW \
                    and event.to_me \
                    and event.text \
                    and event.from_user:
                self.vk_.messages.send(
                    user_id=event.user_id,
                    message="I'm working. wait please!",
                    random_id=randint(dtype="int64", low=0, high=0xffffffff)
                    )
                self.vk_.messages.send(
                    user_id=event.user_id,
                    message='\n'.join(self.make_links(generator.generate(event.user_id))),
                    random_id=randint(dtype="int64", low=0, high=0xffffffff)
                    )
                self.vk_.messages.send(
                    user_id=event.user_id,
                    message="Here are recommendations for you",
                    random_id=randint(dtype="int64", low=0, high=0xffffffff)
                )
