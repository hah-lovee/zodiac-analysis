from rename_me import user_states, QUESTIONS, bot, zodiac_signs

from telebot import types
import csv


def test(message, message_id=None):
    chat_id = message.chat.id
    user_states[chat_id] = {'current_question': 0}
    user_states[chat_id]['answers'] = []
    user_states[chat_id]['test_state'] = True
    ask_next_question(chat_id, message_id=message_id)

def ask_next_question(chat_id, message_id = None):
    question_number = user_states[chat_id]['current_question']
    if question_number < len(QUESTIONS):
        question = QUESTIONS[question_number]
        ask_question(chat_id=chat_id, question=question, message_id=message_id)
    else:
        markup = types.InlineKeyboardMarkup()
        btn_menu = types.InlineKeyboardButton(text="Вернуться в меню", callback_data="menu")
        markup.add(btn_menu)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Спасибо за ответы!", reply_markup=markup)
        print(user_states[chat_id]['answers'])
        user_states[chat_id]['test_state'] = False
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
        if message_id:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=question, reply_markup=markup)
        else :
            bot.send_message(chat_id=chat_id, text=question, reply_markup=markup)

    elif user_states[chat_id]["current_question"] == 1:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text="М", callback_data="М")
        btn2 = types.InlineKeyboardButton(text="Ж", callback_data="Ж")
        markup.add(btn1, btn2)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id ,text=question, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=5)

        btn1 = types.InlineKeyboardButton(text='1', callback_data='zs:0')
        btn2 = types.InlineKeyboardButton(text='2', callback_data='zs:1')
        btn3 = types.InlineKeyboardButton(text='3', callback_data='zs:2')
        btn4 = types.InlineKeyboardButton(text='4', callback_data='zs:3')
        btn5 = types.InlineKeyboardButton(text='5', callback_data='zs:4')

        markup.add(btn1, btn2, btn3, btn4, btn5)
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


@bot.callback_query_handler(func= lambda callback: callback.data in ['1', '2', '3', '4', '5'])
def check_callback_questions(callback):
    chat_id = callback.message.chat.id
    callback_data = int(callback.data)
    user_states[chat_id]['answers'].append(callback_data)
    user_states[chat_id]['current_question'] += 1
    ask_next_question(chat_id, message_id=callback.message.id)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('test_state'))
def handle_unrecognized_commands(message):
    bot.send_message(message.chat.id, "Писать ничего не нужно, просто тыкай☺️")