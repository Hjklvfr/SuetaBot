import random
from typing import Dict

import requests

import telebot
from telebot.types import Message

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)

DICTIONARY: Dict[str, str] = {
    "привет": "Ну, здравствуй"
}

CAT_ANIMATION = "https://cataas.com/cat/gif"
CAT_PHOTO = "https://cataas.com/cat"


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, DICTIONARY["привет"])


def send_cat_photo(chat_id: int):
    response = requests.get(CAT_PHOTO, stream=True)
    bot.send_photo(chat_id, response.content)


def send_cat_gif(chat_id: int):
    response = requests.get(CAT_ANIMATION, stream=True)
    bot.send_video(chat_id, response.content)


@bot.message_handler(commands=["cat"])
def send_cat(message: Message):
    method = random.choice([send_cat_photo, send_cat_gif])
    method(message.chat.id)


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
