import telebot
import sqlite3
import datetime
from random import randint


try:  # Создание БД
    db = sqlite3.connect("actions.db")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE users ( 
        id text,
        action text,
        time text
    )""") # В БД хранятся данные в формате: id пользователя, действие, время
    db.commit()
    db.close()
except:
    pass


def add_to_db(id: int, type: str):  # Функция для добавления события в БД
    time = datetime.datetime.now()
    db = sqlite3.connect("actions.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?, ?);", (str(id), type, f'{time.year}:{time.month}:{time.day} '
                                                                         f'{time.hour}:{time.minute}:{time.second}'))
    cursor.execute("SELECT * FROM users")
    db.commit()
    print(cursor.fetchall())
    db.close()


def count_people(data):  # Функция для подсчета количества людей, совершивших какое-нибудь действие за последний час
    time_now = datetime.datetime.now()
    c = 0
    checked = set()
    for i in data:
        year, month, day, hour, minute, second = list(map(int, i[1].replace(' ', ':').split(':')))
        tm = datetime.datetime(year, month, day, hour, minute, second)
        if (time_now - tm).seconds < 3600 and i[0] not in checked:
            c += 1
            checked.add(i[0])
    return str(c)


STICKERS = ['CAACAgIAAxkBAAEKgVxlJvbvlSc20IVi7kmlPTgNTsyxyAACfxQAAt4kyUvQjArPSHsCpDAE',
            'CAACAgIAAxkBAAEKgV5lJvcxaMnzGIAB3ga2jUUgR0-LnAACsxAAA9HwS2LFcKRpSGsJMAQ',
            'CAACAgIAAxkBAAEKgWBlJvcyjGZTlckO-9xJiSyEYz0CsgACNBIAAhKD-Uv6vzFHb73KAjAE',
            'CAACAgIAAxkBAAEKgWJlJvdAK1S5C42ggFGFrlUwqhw60wAC-REAAuxJ-UvhBonFocPjVDAE',
            'CAACAgIAAxkBAAEKgWRlJvdLN8r6-PJnNrEVhJ64b3bgIQAClhEAAv5tgEmdX9KNHziRpTAE',
            'CAACAgIAAxkBAAEKgWZlJvdXX3ZSfOW1HH7Nhm1KyykPugAC8RcAAjZrYUgtS5ULgfPaLTAE',
            'CAACAgIAAxkBAAEKgWhlJvducZuBCNXOx0kcJZnbwCzrzgACUQQAAvc0GwABBeQ4Db_q22YwBA',
            'CAACAgIAAxkBAAEKgWplJvd_rMfYuAeoWrIOCvrPSqeD6gACmRUAAit1eEh1yI6rouJTiTAE']

API_TOKEN = '6513599781:AAF_cEM6fmSDGIO9BfN7Sy70sPozy1hPIdE'

bot = telebot.TeleBot(API_TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("/admin", "admin")
])


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это бот бизнес-клуба ВШЭ. Для того, чтобы узнать количество пользователей за "
                          "последний час введите команду /admin")


@bot.message_handler(commands=['admin'])
def start_command(message):
    db = sqlite3.connect("actions.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    db.commit()
    data = cursor.fetchall()
    db.close()

    bot.send_message(
        message.chat.id,
        f'Уникальных пользователей за последний час: {count_people([[i[0], i[2]] for i in data])}'
    )


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    add_to_db(message.chat.id, 'message sent')
    bot.send_sticker(message.chat.id, STICKERS[randint(0, 7)])


bot.infinity_polling()
