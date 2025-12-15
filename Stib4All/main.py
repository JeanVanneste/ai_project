#! ../.venv/bin/python

from chatbot import chatbot

bot = chatbot.Chatbot()

bot.chatbot_creation()

while (True):
    human_message = input("> ")
    if human_message == "stop":
        break
    bot.add_user_message(human_message)


print("End of conversation")