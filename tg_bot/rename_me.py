import os
from dotenv import load_dotenv
import telebot

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