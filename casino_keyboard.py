import json
from telebot import types

# Правила
markup_inline_soglashenie = types.InlineKeyboardMarkup()
item_soglashenie = types.InlineKeyboardButton(text="✅ Принять правила", callback_data="soglashenie")
markup_inline_soglashenie.row(item_soglashenie)


# Клавиатура основная
def keyboard_osnova():
    markup_osnova = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('🎮Игры')
    btn2 = types.KeyboardButton('💸Пополнить')
    btn3 = types.KeyboardButton('✨Вывести')
    btn4 = types.KeyboardButton('👤Личный кабинет')
    markup_osnova.row(btn1)
    markup_osnova.add(btn2, btn3)
    markup_osnova.row(btn4)
    return markup_osnova

# Клавиатура с играми
def keyboard_games():
    markup_games = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('🎰Казино')
    btn2 = types.KeyboardButton('📈Crash')
    btn3 = types.KeyboardButton('💰Сейф')
    btn5 = types.KeyboardButton('🧿Рулетка')
    btn4 = types.KeyboardButton('◀️Назад')
    markup_games.row(btn1)
    markup_games.add(btn2, btn3)
    markup_games.row(btn5)
    markup_games.row(btn4)
    return markup_games

# Клавиатура цифры
def keyboard_chifri():
    markup_chifri = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('1️⃣')
    btn2 = types.KeyboardButton('2️⃣')
    btn3 = types.KeyboardButton('3️⃣')
    btn4 = types.KeyboardButton('4️⃣')
    btn5 = types.KeyboardButton('5️⃣')
    markup_chifri.add(btn1, btn2, btn3, btn4, btn5)
    return markup_chifri

# Клавиатура "Назад" при входе в игры
def keyboard_nazad():
    markup_nazad = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('👾Закончить игру')
    markup_nazad.row(btn1)
    return markup_nazad

# "Назад" в функциях добавления админа
def nazad_admin():
    markup_nazad_admin = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню админа')
    markup_nazad_admin.row(btn1)
    return markup_nazad_admin

def nazad_worker():
    markup_nazad_worker = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню воркера')
    markup_nazad_worker.row(btn1)
    return markup_nazad_worker

# Клавиатура с пополнением
def deposit_btn(url):
    deposit_btn = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Оплатить", url=url)
    button2 = types.InlineKeyboardButton(text="🔁Проверить оплату", callback_data="check_payment")
    button3 = types.InlineKeyboardButton(text="❌Отменить  оплату", callback_data="undo_payment")
    deposit_btn.row(button1)
    deposit_btn.add(button2, button3)
    return deposit_btn


# Клавиатура с выводом
def keyboard_vivod():
    markup_vivod = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('◀️Назад')
    markup_vivod.row(btn1)
    return markup_vivod


# Клавиатура администратора
def keyboard_admin():
    markup_admin = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Изменить баланс')
    btn2 = types.KeyboardButton('Сделать рассылку')
    btn8 = types.KeyboardButton('Сделать рассылку воркерам')
    btn9 = types.KeyboardButton('Фейк залёт')
    btn3 = types.KeyboardButton('Изменить статус')
    btn4 = types.KeyboardButton('Добавить воркера')
    btn5 = types.KeyboardButton('Удалить воркера')
    btn6 = types.KeyboardButton('Информация')
    btn7 = types.KeyboardButton('Выйти')
    markup_admin.row(btn2)
    markup_admin.row(btn8)
    markup_admin.add(btn9)
    markup_admin.add(btn1, btn3)
    markup_admin.add(btn4, btn5)
    markup_admin.row(btn6)
    markup_admin.row(btn7)
    return markup_admin


# Клавитура воркера
def keyboard_worker():
    markup_worker = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Изменить баланс')
    btn5 = types.KeyboardButton('Изменить статус')
    btn2 = types.KeyboardButton('Профиль')
    btn3 = types.KeyboardButton('Информация')
    btn4 = types.KeyboardButton('Выйти')
    markup_worker.add(btn1, btn5)
    markup_worker.row(btn2, btn3)
    markup_worker.row(btn4)
    return markup_worker
    


# Клавиатура с исходом
def bet():
    markup_bet = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('< 50')
    btn2 = types.KeyboardButton('= 50')
    btn3 = types.KeyboardButton('> 50')
    btn4 = types.KeyboardButton('👾Закончить игру')
    markup_bet.add(btn1, btn2, btn3)
    markup_bet.row(btn4)
    return markup_bet

def roulette_bet():
    markup_bet = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('1-12')
    btn2 = types.KeyboardButton('13-24')
    btn3 = types.KeyboardButton('25-36')
    btn5 = types.KeyboardButton('Чётное')
    btn6 = types.KeyboardButton('Нечётное')
    btn4 = types.KeyboardButton('👾Закончить игру')
    markup_bet.add(btn1, btn2, btn3)
    markup_bet.row(btn5, btn6)
    markup_bet.row(btn4)
    return markup_bet

# Клавиатура с сейфами
def bet_2():
    markup_bet_2 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('🗄')
    btn2 = types.KeyboardButton('🗄')
    btn3 = types.KeyboardButton('👾Закончить игру')
    markup_bet_2.add(btn1, btn2)
    markup_bet_2.row(btn3)
    return markup_bet_2

def bet_3():
    markup_bet_3 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Приготовиться к игре')
    btn2 = types.KeyboardButton('👾Закончить игру')
    markup_bet_3.row(btn1)
    markup_bet_3.row(btn2)
    return markup_bet_3

def bet_4():
    markup_bet_4 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Забрать выигрыш')
    markup_bet_4.row(btn1)
    return markup_bet_4

def bet_5():
    markup_bet_5 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Играть снова')
    markup_bet_5.row(btn1)
    return markup_bet_5

def keyboard_deposit_methods():
    keyboard_deposit = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('💳Карта')
    btn2 = types.KeyboardButton('🥝Qiwi')
    btn3 = types.KeyboardButton('◀️Назад')
    keyboard_deposit.add(btn1, btn2)
    keyboard_deposit.row(btn3)
    return keyboard_deposit

def del_msg_button():
    del_msg_button = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Закрыть❌", callback_data="del_msg")
    del_msg_button.row(button)
    return del_msg_button

def payment_keyboard(payment_id):
    payment_keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="80%", callback_data=f"80%:{payment_id}")
    button2 = types.InlineKeyboardButton(text="70% ТП", callback_data=f"70%:{payment_id}")
    button3 = types.InlineKeyboardButton(text="X2", callback_data=f"x_payment2:{payment_id}")
    button4 = types.InlineKeyboardButton(text="X3", callback_data=f"x_payment3:{payment_id}")
    button5 = types.InlineKeyboardButton(text="X4", callback_data=f"x_payment4:{payment_id}")
    payment_keyboard.row(button1, button2)
    payment_keyboard.add(button3, button4, button5)
    return payment_keyboard
