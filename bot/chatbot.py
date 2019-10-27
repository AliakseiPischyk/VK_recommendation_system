import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from numpy.random import randint


class ChatBot:
    def __init__(self, token):
        vk_session = vk.VkApi(token=token)
        self.longPoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def run(self, generator):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW \
                    and event.to_me \
                    and event.text \
                    and event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message=generator.generate(),
                    random_id=randint(dtype="int64")
                    )
