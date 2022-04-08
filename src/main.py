from typing import Dict

import requests

import telebot
from telebot.types import Message

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)

DICTIONARY: Dict[str, str] = {
    "привет": "Ну, здравствуй"
}


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, DICTIONARY["привет"])


@bot.message_handler(commands=["cat"])
def send_cat(message: Message):
    response = requests.get("https://cataas.com/cat", stream=True)
    bot.send_photo(message.chat.id, response.content)


def is_message_from_dictionary(message: Message):
    dict_key = next(filter(lambda x: x == message.text.lower(), DICTIONARY.keys()), None)
    return dict_key is not None


@bot.message_handler(func=lambda x: True)
def send_reply(message: Message):
    if is_message_from_dictionary(message):
        bot.reply_to(message, DICTIONARY[message.text.lower()])
    else:
        bot.reply_to(message, "Не могу ответить")


if __name__ == "__main__":
    bot.infinity_polling()
