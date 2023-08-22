import telebot

import csv
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)

user_states = {}

QUESTIONS = [
    "Введите ваш знак зодиака",
    "Введите ваш пол",
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
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("👋 Поздороваться")
    # markup.add(btn1)
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

def ask_next_question(chat_id):
    question_number = user_states[chat_id]['current_question']
    if question_number < len(QUESTIONS):
        question = QUESTIONS[question_number]
        # Добавить кнопки нормальные к вопросам
        bot.send_message(chat_id, question)
        user_states[chat_id]['waiting_for_answer'] = True
    else:
        bot.send_message(chat_id, "Спасибо за ответы!")
        user_states[chat_id]['waiting_for_answer'] = False
        print(user_states[chat_id]['answers'])

        with open("data.csv", mode="a", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(user_states[chat_id]['answers'])
        user_states[chat_id]['answers'] = []


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('waiting_for_answer'))
def reply_with_answer(message):
    chat_id = message.chat.id
    user_answer = message.text
    validate_answers(chat_id, user_answer)
    ask_next_question(chat_id)

def validate_answers(chat_id, answer):
    # обработка зз 
    # сделать словарём, чтоб сразу кодировать в цифры
    if user_states[chat_id]["current_question"] == 0:
        if answer.lower() in zodiac_signs:
            user_states[chat_id]['answers'].append(answer)
            user_states[chat_id]['current_question'] += 1
        else:
            bot.send_message(chat_id, "такого нету :(")
    # обработка пола
    elif user_states[chat_id]["current_question"] == 1:
        if answer.lower() == "м":
            user_states[chat_id]['answers'].append(0)
            user_states[chat_id]['current_question'] += 1
        elif answer.lower() == "ж":
            user_states[chat_id]['answers'].append(1)
            user_states[chat_id]['current_question'] += 1
        else:
            bot.send_message(chat_id, "м/ж")
    else:
        if answer.isdigit() and int(answer) in range(1,6):
            user_states[chat_id]['answers'].append(answer)
            user_states[chat_id]['current_question'] += 1
        else:
            # user_states[chat_id]["current_question"] -= 1
            bot.send_message(chat_id, "Попробуй число от 1 до 5")
        

@bot.message_handler(func=lambda message: True)
def handle_unrecognized_commands(message):
    bot.send_message(message.chat.id, "Извините, я не понимаю эту команду.")

print("Starting...")
bot.polling(none_stop=True)
