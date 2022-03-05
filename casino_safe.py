import sqlite3
import random
from casino_config import bot, get_balance, get_last_popolnenie, get_status
from casino_keyboard import keyboard_osnova, keyboard_nazad, bet_2



# Сейф начинает работу
def play_safe(message):
    balance = get_balance(message)
    bot.send_message(message.from_user.id, f"Введите сумму ставки \n\nВаш баланс: {balance}0₽",
                     reply_markup=keyboard_nazad())
    bot.register_next_step_handler(message, play_safe_2)


# Сейф игра
def play_safe_2(message):
    balance = get_balance(message)

    if message.text == "👾Закончить игру":
        bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                         reply_markup=keyboard_osnova())
        from casino_bot import get_text_message
        bot.register_next_step_handler(message, get_text_message)

    elif message.text.isdigit() and int(message.text) >= 0 and balance >= int(message.text):
        stavka = int(message.text)
        bot.send_message(message.from_user.id,
                         "Выберите 1 из 2 сейфов, если Вы выберите нужный сейф, то получите x3 от Вашей ставки",
                         reply_markup=bet_2())
        bot.register_next_step_handler(message, play_safe_3, stavka)

    else:
        bot.send_message(message.from_user.id, "На Вашем счету недостаточно средств")
        play_safe(message)


def play_safe_3(message, stavka):
    con = sqlite3.connect("dannie_2.db")
    cur = con.cursor()
    status = get_status(message)
    balance = get_balance(message)
    last_popolnenie = get_last_popolnenie(message)
    finish_popolnenie = last_popolnenie * 4.8
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

    stavka = stavka
    bet = message.text
    status = get_status(message)

    if bet == "🗄":

     if status == 0:
        bot.send_message(message.from_user.id, f"Вы выиграли!")
        balance = balance - stavka + stavka * 3
        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
        con.commit()
        play_safe(message)

     elif status == 1:
        balances = balance - stavka + stavka * 2
        if balances < (last_popolnenie * 4.9):
            bot.send_message(message.from_user.id, f"Вы выиграли!")
            balance = balance - stavka + stavka * 3
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_safe(message)
        else:
            bot.send_message(message.from_user.id, f"Вы проиграли!")
            balance = balance - stavka
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_safe(message)

     elif status == 2:
        balances = balance - stavka + stavka * 2
        if balances < (last_popolnenie * 4.9):
            number = random.choice(range(20, 100))
            if number < 50:
                bot.send_message(message.from_user.id, f"Вы выиграли!")
                balance = balance - stavka + stavka * 3
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_safe(message)
            else:
                bot.send_message(message.from_user.id, f"Вы проиграли!")
                balance = balance - stavka
                cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
                con.commit()
                play_safe(message)
        else:
            bot.send_message(message.from_user.id, f"Вы проиграли!")
            balance = balance - stavka
            cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
            con.commit()
            play_safe(message)

     elif status == 3:
        bot.send_message(message.from_user.id, f"Вы проиграли!")
        balance = balance - stavka
        cur.execute(f"UPDATE users SET balance = {balance} WHERE id = {message.chat.id}")
        con.commit()
        play_safe(message)

    elif bet == "Закончить игру":
     bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
                 reply_markup=keyboard_osnova())
     from casino_bot import get_text_message

     bot.register_next_step_handler(message, get_text_message)