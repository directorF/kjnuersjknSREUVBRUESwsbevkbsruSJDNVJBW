import sqlite3
import json
import random
from requests import get
from telebot import types
from casino_functions import add_deposit, add_balance, check_deposit, add_conclusion, \
    get_conclusion, get_user_balance, get_deposit_amount, get_username, get_boss, add_payment, \
    get_worker_username
from casino_config import bot, get_balance, get_last_popolnenie, get_status, get_referals, get_ref_balance, \
    get_ref_link, get_random_number, get_inf_profil, QIWI_NUMBER, QIWI_TOKEN, admin_1, admin_chat, conclusion_channel, \
    workers_chat, min_deposit, percent
from casino_keyboard import keyboard_osnova, keyboard_nazad, bet_2, bet_3, bet_4, \
    bet_5, del_msg_button, payment_keyboard
from casino_money import _set_bill_id, _create_invoice

start_game = types.InlineKeyboardMarkup(row_width=1)
start_game.add(types.InlineKeyboardButton(text='Я готов! 😎', callback_data='start'))


# Краш начинает работу
def play_crash(message):
    balance = get_balance(message)
    bot.send_message(message.from_user.id, f"Введите сумму ставки \n\nВаш баланс: {balance}0₽",
                     reply_markup=keyboard_nazad())
    bot.register_next_step_handler(message, play_crash_2)


# Краш игра
def play_crash_2(message):
    balance = get_balance(message)

    if message.text == "👾Закончить игру":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)

    elif message.text.isdigit() and int(message.text) >= 0 and balance >= int(message.text):
        stavkas = int(message.text)
        bot.send_message(message.from_user.id,
                         "Введите коээфициент, на котором хотите забрать ставку (От 2 до 30)\n\nКаждую секунду коэффициент, на который будет умножена Ваша ставка, будет увеличиваться. Если Вы успеет забрать свою ставку до того, как коэффициент перестанет расти, то получите сумму, которая = Ваша ставка * последний коэффициент. В противном случае Вы потеряете сумму, равную Вашей ставки")
        bot.register_next_step_handler(message, play_crash_3, stavkas)

    else:
        bot.send_message(message.from_user.id, "На Вашем счету недостаточно средств")
        play_crash(message)


def play_crash_3(message, stavkas):
    if message.text == "Закончить игру":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)

    elif message.text.isdigit() and 30 >= int(message.text) >= 2:
        coefficients = int(message.text)
        bot.send_message(message.from_user.id, "Примите решение", reply_markup=bet_3())
        bot.register_next_step_handler(message, play_crash_4, stavkas, coefficients)

    else:
        bot.send_message(message.from_user.id, "Упс, что-то пошло не так")
        play_crash(message)


def play_crash_4(message, stavkas, coefficients):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    status = get_status(message)
    balance = get_balance(message)
    last_popolnenie = get_last_popolnenie(message)
    finish_popolnenie = last_popolnenie * 4.5
    if status != 0 and finish_popolnenie <= balance:
        status = 3
        cur.execute(f"UPDATE users SET status = {status} WHERE id = {message.chat.id}")
        con.commit()
    elif status == 3 and last_popolnenie * 4 >= balance:
        status = 2
        cur.execute(f"UPDATE users SET status = {status} WHERE id = {message.chat.id}")
        con.commit()

    else:
        pass

    bet = message.text

    global stavka
    stavka = stavkas

    global coefficient
    coefficient = coefficients

    if bet == "Приготовиться к игре":
        bot.send_message(message.from_user.id, "Нажми на меня", reply_markup=start_game)
        bot.send_photo(message.chat.id, get(
            "https://monolitestate.com/assets/images/resources/17226/sm/rabstol-net-quotes-05.jpg").content)

    elif bet == "👾Закончить игру":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)


# Ответы
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    chat_id = call.message.chat.id
    message_id=call.message.message_id
    id = call.message.chat.id
    if chat_id > 0:
        if call.data == "start":
            con = sqlite3.connect("dannie_2.db")
            cur = con.cursor()
            status = get_status(call.message)
            balance = get_balance(call.message)
            last_popolnenie = get_last_popolnenie(call.message)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f'0', )

            if status == 0:
                if coefficient > 25:
                    finite_number = random.choice(range(25, 31))
                    for i in range(1, finite_number + 1):
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=f'{i}', )
                    bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                    if coefficient == finite_number:
                        balance = balance - stavka + stavka * coefficient
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)
                    else:
                        balance = balance - stavka
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)

                else:
                    random_number = random.choice(range(2, 5))
                    finite_number = random_number + coefficient
                    for i in range(1, finite_number + 1):
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=f'{i}', )
                    bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                    balance = balance - stavka + stavka * coefficient
                    cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                    con.commit()
                    bot.register_next_step_handler(call.message, play_crash)



            elif status == 1:
                balances = balance - stavka + stavka * coefficient
                if balances < (last_popolnenie * 4.9):
                    if coefficient > 25:
                        finite_number = random.choice(range(25, 31))
                        for i in range(1, finite_number + 1):
                            bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'{i}', )
                        bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                        if coefficient == finite_number:
                            balance = balance - stavka + stavka * coefficient
                            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                            con.commit()
                            bot.register_next_step_handler(call.message, play_crash)
                        else:
                            balance = balance - stavka
                            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                            con.commit()
                            bot.register_next_step_handler(call.message, play_crash)
                    else:
                        random_number = random.choice(range(2, 5))
                        finite_number = random_number + coefficient
                        for i in range(1, finite_number + 1):
                            bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'{i}', )
                        bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                        balance = balance - stavka + stavka * coefficient
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)
                else:
                    if coefficient > 3:
                        random_number = random.choice(range(1, 3))
                        finite_number = coefficient - random_number
                        for i in range(1, finite_number + 1):
                            bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'{i}', )
                        bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!",
                                         reply_markup=bet_5())
                        balance = balance - stavka
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)
                    else:
                        bot.send_message(call.message.chat.id, "Коэффициент остановился на цифре 0!", reply_markup=bet_5())
                        balance = balance - stavka
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)



            elif status == 2:
                balances = balance - stavka + stavka * coefficient
                if balances < (last_popolnenie * 4.9):
                    random_number = random.choice(range(1, 4))
                    if random_number == 1:
                        if coefficient > 25:
                            finite_number = random.choice(range(25, 31))
                            for i in range(1, finite_number + 1):
                                bot.edit_message_text(
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'{i}', )
                            bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                            if coefficient == finite_number:
                                balance = balance - stavka + stavka * coefficient
                                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                                con.commit()
                                bot.register_next_step_handler(call.message, play_crash)
                            else:
                                balance = balance - stavka
                                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                                con.commit()
                                bot.register_next_step_handler(call.message, play_crash)
                        else:
                            random_number = random.choice(range(2, 5))
                            finite_number = random_number + coefficient
                            for i in range(1, finite_number + 1):
                                bot.edit_message_text(
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'{i}', )
                            bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!", )
                            balance = balance - stavka + stavka * coefficient
                            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                            con.commit()
                            bot.register_next_step_handler(call.message, play_crash)
                    else:
                        if coefficient > 3:
                            random_number = random.choice(range(1, 3))
                            finite_number = coefficient - random_number
                            for i in range(1, finite_number + 1):
                                bot.edit_message_text(
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'{i}', )
                            bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!",
                                             reply_markup=bet_5())
                            balance = balance - stavka
                            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                            con.commit()
                            bot.register_next_step_handler(call.message, play_crash)
                        else:
                            bot.send_message(call.message.chat.id, "Коэффициент остановился на цифре 0!",
                                             reply_markup=bet_5())
                            balance = balance - stavka
                            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                            con.commit()
                            bot.register_next_step_handler(call.message, play_crash)
                else:
                    if coefficient > 3:
                        random_number = random.choice(range(1, 3))
                        finite_number = coefficient - random_number
                        for i in range(1, finite_number + 1):
                            bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f'{i}', )
                        bot.send_message(call.message.chat.id, f"Коэффициент остановился на цифре {finite_number}!",
                                         reply_markup=bet_5())
                        balance = balance - stavka
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)
                    else:
                        bot.send_message(call.message.chat.id, "Коэффициент остановился на цифре 0!", reply_markup=bet_5())
                        balance = balance - stavka
                        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                        con.commit()
                        bot.register_next_step_handler(call.message, play_crash)



            elif status == 3:
                bot.send_message(call.message.chat.id, "Коэффициент остановился на цифре 0!", reply_markup=bet_5())
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {call.message.chat.id}")
                con.commit()
                bot.register_next_step_handler(call.message, play_crash)



        elif call.data == "soglashenie":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            balance = get_balance(call.message)
            referals = get_referals(call.message)
            ref_balance = get_ref_balance(call.message)
            ref_link = get_ref_link(call.message)
            random_number = get_random_number(call.message)
            inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link, random_number)
            bot.send_message(call.message.chat.id, f"{inf_profil}", reply_markup=keyboard_osnova())

        elif call.data == "check_payment":
            status = 'Обработка'
            answer, amount = check_deposit(id, QIWI_NUMBER, QIWI_TOKEN, 10)
            if answer:
                if amount >= min_deposit:
                    if amount == get_deposit_amount(id):
                        add_balance(id, amount)
                        balance = get_user_balance(id)
                        bot.send_message(id, f"Ваш баланс успешно пополнен и составляет: {balance}₽")
                        bot.send_message(admin_1, f"На ваш киви поступил платеж на сумму: {amount}₽")
                        code = random.randint(1111111, 9999999)
                        worker = get_boss(id)
                        worker_username = get_worker_username(worker)
                        bot.send_message(admin_chat,
                                            f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                            f"🎅Воркер: @{worker_username} 🎅\n"
                                            f"🎄Сумма: {amount}₽ 🎄\n"
                                            f"ID Мамонта: {id}\n", reply_markup=payment_keyboard(code))
                        add_payment(worker, amount)
                        add_conclusion(amount, worker_username, id, code)
                        add_deposit(id)
                    else:
                        bot.send_message(id, f"Вы указали неверную сумму при переводе!❌",
                        reply_markup=del_msg_button())
                else:
                    pass
            else:
                bot.send_message(id, f"Платеж не найден!❌",
                        reply_markup=del_msg_button())
        
        
                                        
        elif call.data == "undo_payment":
            bot.delete_message(chat_id=id, message_id=message_id)
            bot.send_message(id, f"Платеж успешно отменён.")
        
        elif call.data == 'del_msg':
            bot.delete_message(chat_id=id, message_id=message_id)

    else:
        if call.data.startswith("80%"):
            percent = 20
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
            status = '🔄Обработка'
            payment_id = call.data.split(":")[1]
            payment = get_conclusion(payment_id)
            bot.send_message(conclusion_channel,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n"
                                    f"❄️ДОЛЯ ВОРКЕРА: {round(payment[0]-payment[0]/100*percent)}₽ ❄️\n"
                                    f"✅СТАТУС: {status}\n")
            bot.send_message(workers_chat,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n")

        elif call.data.startswith("70%"):
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
            status = '🔄Обработка'
            percent = 30
            payment_id = call.data.split(":")[1]
            payment = get_conclusion(payment_id)
            bot.send_message(conclusion_channel,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n"
                                    f"❄️ДОЛЯ ВОРКЕРА: {round(payment[0]-payment[0]/100*percent)}₽ ❄️\n"
                                    f"❄️(С помощью: @SeniorCasinoSupport 70%)\n"
                                    f"✅СТАТУС: {status}\n")
            bot.send_message(workers_chat,
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n")


        elif call.data.startswith("x_payment"):
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
            x = call.data[9:10]
            if x == "2":
                percent = 30
            elif x == "3":
                percent = 40
            else:
                percent = 40
            status = '🔄Обработка'
            payment_id = call.data.split(":")[1]
            payment = get_conclusion(payment_id)
            bot.send_message(conclusion_channel,
                                    f"💳X{x} ОПЛАТА\n"
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n"
                                    f"❄️ДОЛЯ ВОРКЕРА: {round(payment[0]-payment[0]/100*percent)}₽ ❄️\n"
                                    f"✅СТАТУС: {status}\n")
            bot.send_message(workers_chat,
                                    f"💳X{x} ОПЛАТА\n"
                                    f"💰МАМОНТ ПОПОЛНИЛ БАЛАНС💰  \n"
                                    f"🎅Воркер: @{payment[2]} 🎅\n"
                                    f"🎄Сумма: {payment[0]}₽ 🎄\n")
        else:
            pass