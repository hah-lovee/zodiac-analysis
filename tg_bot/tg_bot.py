from test_handler import test
from rename_me import bot

import telebot
from telebot import types



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_menu = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
    markup.add(btn_menu)
    bot.send_message(message.from_user.id, "Привет, предлагаю пройти тест."
                      "Для большей информации нажми на /help", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "/start — Показывает вступительные слова\n"
                     "/help — Выводит этот текст\n"
                     "/test — начинает тест")


@bot.message_handler(commands=['test'])
def handler_test_command(message):
    test(message)

@bot.callback_query_handler(func= lambda callback: callback.data == "test")
def handler_test_button(callback):
    test(callback.message, callback.message.id)


@bot.callback_query_handler(func= lambda callback: callback.data == "menu")
def callback_menu(callback):
    markup = menu_create()
    bot.edit_message_text(chat_id=callback.message.chat.id, 
                          message_id=callback.message.id,
                          text='Главное меню', 
                          reply_markup=markup)

# menu -> markup
def menu_create():
    markup = types.InlineKeyboardMarkup()
    btn_test = types.InlineKeyboardButton(text='Пройти тест', callback_data='test')
    markup.add(btn_test)
    return markup

@bot.message_handler(func=lambda message: True)
def handle_unrecognized_commands(message):
    bot.send_message(message.chat.id, "Извините, я не понимаю эту команду.")


print("Starting...")
bot.polling(none_stop=True)
