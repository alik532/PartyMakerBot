from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_kb = ReplyKeyboardMarkup()
cancel_bttn = KeyboardButton('/Отменить')

cancel_kb.add(cancel_bttn)