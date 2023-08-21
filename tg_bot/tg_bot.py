import telebot

import csv
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

token = os.environ['TOKEN']

bot = telebot.TeleBot(token)

user_states = {}

QUESTIONS = [
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

@bot.message_handler(commands=['start'])
def start(message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("👋 Поздороваться")
    # markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет, предлагаю пройти тест. Для большей информации нажми на /help")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "/start — Показывает вступительные слова\n/help — Выводит этот текст\n/test — начинает тест")

@bot.message_handler(commands=['test'])
def test(message):
    user_states[message.chat.id] = {'current_question': 0}
    user_states[message.chat.id]['answers'] = []
    ask_next_question(message.chat.id)

def ask_next_question(chat_id):
    question_number = user_states[chat_id]['current_question']
    if question_number < len(QUESTIONS):
        question = QUESTIONS[question_number]
        bot.send_message(chat_id, question)
        user_states[chat_id]['current_question'] += 1
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
    # Сделать отдельную функцию проверки, тк будут ещё ответы в виде строк(пол и знак зодиака)
    if user_answer.isdigit() and int(user_answer) in range(1,6):
        user_states[chat_id]['answers'].append(user_answer)
    else:
        user_states[chat_id]["current_question"] -= 1
        bot.send_message(chat_id, "Попробуй число от 1 до 5")
    

    ask_next_question(chat_id)


@bot.message_handler(func=lambda message: True)
def handle_unrecognized_commands(message):
    bot.send_message(message.chat.id, "Извините, я не понимаю эту команду.")

# @bot.message_handler(content_types=['text'])  #реагирует на любые сообщения
# def text(message):
#     pass

bot.polling(none_stop=True)