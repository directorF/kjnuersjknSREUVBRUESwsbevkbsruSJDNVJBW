import sqlite3
import random
from casino_config import bot, get_balance, get_last_popolnenie, get_status
from casino_keyboard import keyboard_osnova, keyboard_nazad, roulette_bet


# Рулетка начинает работу
def play_roulette(message):
    balance = get_balance(message)
    bot.send_message(message.from_user.id, f"Введите сумму ставки \n\n💰Ваш баланс: {balance}0₽", reply_markup=keyboard_nazad())
    bot.register_next_step_handler(message, play_roulette_2)

def play_roulette_2(message):
	balance = get_balance(message)

	if message.text == "👾Закончить игру":
		bot.send_message(message.from_user.id, "😔 Очень жаль, что Вы так мало решили поиграть 😔",
							reply_markup=keyboard_osnova())
		from casino_bot import get_text_message
		bot.register_next_step_handler(message, get_text_message)
	elif message.text.isdigit() and int(message.text) >= 0 and balance >= int(message.text):
		bet_amount = int(message.text)
		bot.send_message(message.from_user.id, "Сейчас прокрутится рулетка\nВыберите исход события",
								reply_markup=roulette_bet())
		bot.register_next_step_handler(message, play_roulette_3, bet_amount)
	else:
		bot.send_message(message.from_user.id, "На Вашем счету недостаточно средств")
		play_roulette(message)

def play_roulette_3(message, bet_amount):
	db = sqlite3.connect("dannie_2.db")
	cursor = db.cursor()

	balance = get_balance(message)
	bet = message.text
	status = get_status(message)
	
	if bet == "1-12":
		if status == 0:
			
			number = random.randint(1, 12)
			balance += bet_amount * 2
			cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
			db.commit()
			bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
			play_roulette(message)

		elif status == 1:
			number = random.randint(1, 36)
			if number >= 1 and number <= 12:
				balance += bet_amount * 2
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
				play_roulette(message)
			
			else:
				balance -= bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"😔Вы проиграли! Выпало число {number}")
				play_roulette(message)

	elif bet == "13-24":
		if status == 0:
			
			number = random.randint(13, 24)
			balance += bet_amount * 2
			cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
			db.commit()
			bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
			play_roulette(message)

		
		elif status == 1:
			number = random.randint(1, 36)
			if number >= 13 and number <= 24:
				balance += bet_amount * 2
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
				play_roulette(message)
			
			else:
				balance -= bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"😔Вы проиграли! Выпало число {number}")
				play_roulette(message)

	elif bet == "25-36":
		if status == 0:
			
			number = random.randint(25, 36)
			balance += bet_amount * 2
			cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
			db.commit()
			bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
			play_roulette(message)

		
		elif status == 1:
			number = random.randint(1, 36)
			if number >= 25 and number <= 36:
				balance += bet_amount * 2
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
				play_roulette(message)
			
			else:
				balance -= bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"😔Вы проиграли! Выпало число {number}")
				play_roulette(message)

	elif bet == "Чётное":
		if status == 0:
			numbers = range(1, 36)
			numbers = [x for x in numbers if not x%2]
			number = random.choice(numbers)
			balance += bet_amount
			cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
			db.commit()
			bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
			play_roulette(message)

		
		elif status == 1:
			number = random.randint(1, 36)
			if number % 2 == 0:
				balance += bet_amount * 2
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
				play_roulette(message)
			
			else:
				balance -= bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"😔Вы проиграли! Выпало число {number}")
				play_roulette(message)

	elif bet == "Нечётное":
		if status == 0:
			numbers = range(1, 36)
			numbers = [x for x in numbers if x%2]
			number = random.choice(numbers)
			balance += bet_amount
			cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
			db.commit()
			bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
			play_roulette(message)

		
		elif status == 1:
			number = random.randint(1, 36)
			if number % 2 != 0:
				balance += bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"🎉Вы выиграли! Выпало число {number}")
				play_roulette(message)
			
			else:
				balance -= bet_amount
				cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE id = '{message.from_user.id}' """)
				db.commit()
				bot.send_message(message.from_user.id, f"😔Вы проиграли! Выпало число {number}")
				play_roulette(message)