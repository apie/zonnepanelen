#!/usr/bin/env python3
import telebot
from bot_config import TOKEN
from save_usage import save_current_usage
from print_usage import list_current_usage

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['usage'])
def send_usage(message):
    save_current_usage()
    bot.reply_to(message, list_current_usage())

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()

