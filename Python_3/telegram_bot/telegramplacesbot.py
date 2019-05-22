from database import *
import telebot
from collections import defaultdict


token = '734459503:AAGi401ZUkNQhMmVCg-lALReUFw7IDar06Y'


START, TITLE, LOCATION, ADDRESS, CONFIRMATION = range(5)


bot = telebot.TeleBot(token)


USER_STATE = defaultdict(lambda: START)


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


@bot.message_handler(func=lambda message: get_state(message))
def handle_message(message):



bot.polling()