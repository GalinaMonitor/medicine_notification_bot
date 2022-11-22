from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_intro_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardMarkup(resize_keyboard=True)
	kb.add(KeyboardButton('Добавить пациента'))
	kb.insert(KeyboardButton('Найти пациента по номеру истории болезни'))
	kb.add(KeyboardButton('Напоминания на сегодня'))
	return kb


def get_cancel_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardMarkup(resize_keyboard=True)
	kb.add(KeyboardButton('/cancel'))

	return kb


def get_true_or_false() -> InlineKeyboardMarkup:
	kb = InlineKeyboardMarkup(row_width=1)
	kb.insert(InlineKeyboardButton(text='Да', callback_data='True'))
	kb.insert(InlineKeyboardButton(text='Нет', callback_data='False'))
	return kb
