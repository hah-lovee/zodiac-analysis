import telebot
from telebot import types

import csv
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)

user_states = {}

QUESTIONS = [
    "Выберите ваш знак зодиака",
    "Выберите ваш пол",
    "Question 1: What is 2 + 2?",
    "Question 2: enter a number from 1 to 5",
    "Question 3: enter a number from 1 to 5",
    "Question 4: enter a number from 1 to 5",
    # "Question 5: enter a number from 1 to 5",
    # "Question 6: enter a number from 1 to 5",
    # "Question 7: enter a number from 1 to 5",
    # "Question 8: enter a number from 1 to 5",
    # "Question 9: enter a number from 1 to 5",
    # "Question 10: enter a number from 1 to 5",

]

zodiac_signs = [
    "овен",
    "телец",
    "близнецы",
    "рак",
    "лев",
    "дева",
    "весы",
    "скорпион",
    # "змееносец",
    "стрелец",
    "козерог",
    "водолей",
    "рыбы",
]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, предлагаю пройти тест."
                      "Для большей информации нажми на /help")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "/start — Показывает вступительные слова\n"
                     "/help — Выводит этот текст\n"
                     "/test — начинает тест")

@bot.message_handler(commands=['test'])
def test(message):
    user_states[message.chat.id] = {'current_question': 0}
    user_states[message.chat.id]['answers'] = []
    ask_next_question(message.chat.id)

def ask_next_question(chat_id, message_id = None):
    question_number = user_states[chat_id]['current_question']
    if question_number < len(QUESTIONS):
        question = QUESTIONS[question_number]
        ask_question(chat_id=chat_id, question=question, message_id=message_id)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Спасибо за ответы!")
        print(user_states[chat_id]['answers'])

        with open("data.csv", mode="a", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(user_states[chat_id]['answers'])
        user_states[chat_id]['answers'] = []


def ask_question(chat_id, question, message_id):
    if user_states[chat_id]["current_question"] == 0:
        # вставлять в ряд по 4/3/2 зз
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(0, len(zodiac_signs), 3):
            btn1 = types.InlineKeyboardButton(text=zodiac_signs[i], callback_data='zs:'+str(i))
            btn2 = types.InlineKeyboardButton(text=zodiac_signs[i+1], callback_data='zs:'+str(i+1))
            btn3 = types.InlineKeyboardButton(text=zodiac_signs[i+2], callback_data='zs:'+str(i+2))
            # btn4 = types.InlineKeyboardButton(text=zodiac_signs[i+3], callback_data=zodiac_signs[i+3])
            
            markup.add(btn1, btn2, btn3)
        bot.send_message(chat_id=chat_id, text=question, reply_markup=markup)
    elif user_states[chat_id]["current_question"] == 1:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text="М", callback_data="М")
        btn2 = types.InlineKeyboardButton(text="Ж", callback_data="Ж")
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id ,text=question, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in range(1, 4, 2):
            btn1 = types.InlineKeyboardButton(text=str(i), callback_data=i)
            btn2 = types.InlineKeyboardButton(text=str(i+1), callback_data=i+1)

            markup.add(btn1, btn2)
        btn = types.InlineKeyboardButton(text='5', callback_data=5)
        markup.add(btn)

        bot.edit_message_text(chat_id=chat_id, message_id=message_id ,text=question, reply_markup=markup)


@bot.callback_query_handler(func= lambda callback: 'zs:' in callback.data)
def check_callback_zodiac_sings(callback):
    chat_id = callback.message.chat.id
    callback_data = int( callback.data.split(':')[1] )
    print(callback_data, zodiac_signs[callback_data])
    user_states[chat_id]['answers'].append(callback_data)
    user_states[chat_id]['current_question'] += 1
    ask_next_question(chat_id, message_id=callback.message.id)


@bot.callback_query_handler(func= lambda callback: callback.data in ["М", "Ж"])
def check_callback_male(callback):
    chat_id = callback.message.chat.id
    callback_data = callback.data
    if callback_data == "M":
        user_states[chat_id]['answers'].append(0)
    else :
        user_states[chat_id]['answers'].append(1)
    user_states[chat_id]['current_question'] += 1
    ask_next_question(chat_id , message_id=callback.message.id)


@bot.callback_query_handler(func= lambda callback: int(callback.data) in range(1, 6))
def check_callback_questions(callback):
    chat_id = callback.message.chat.id
    callback_data = int(callback.data)
    user_states[chat_id]['answers'].append(callback_data)
    user_states[chat_id]['current_question'] += 1
    ask_next_question(chat_id, message_id=callback.message.id)


@bot.message_handler(func=lambda message: True)
def handle_unrecognized_commands(message):
    bot.send_message(message.chat.id, "Извините, я не понимаю эту команду.")


print("Starting...")
bot.polling(none_stop=True)
