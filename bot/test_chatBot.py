from unittest import TestCase

from bot.chatbot import ChatBot


class TestChatBot(TestCase):
    def test_make_links(self):
        bot = ChatBot()
        actual = bot.make_links([1,2,3])
        expected = ["https://vk.com/id1","https://vk.com/id2","https://vk.com/id3"]
        assert(actual==expected)

    def test_make_links_empty(self):
        bot = ChatBot()
        actual = bot.make_links([])
        expected = []
        assert(actual==expected)