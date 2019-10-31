from bot.chatbot import ChatBot
from contentGenerators.FriendFinder import FriendFinder

bot = ChatBot()
gen = FriendFinder()
bot.run(gen)
