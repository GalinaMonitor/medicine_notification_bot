from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_intro_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardMarkup(resize_keyboard=True)
	kb.add(KeyboardButton('Добавить пациента'))
	kb.insert(KeyboardButton('Найти пациента по номеру истории болезни'))
	kb.add(KeyboardButton('Напоминания на сегодня'))
	kb.insert(KeyboardButton('Редактировать профиль'))
	kb.add(KeyboardButton('Получить excel-файл'))
	return kb


def get_cancel_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardMarkup(resize_keyboard=True)
	kb.add(KeyboardButton('Вернуться'))

	return kb


def get_true_or_false() -> InlineKeyboardMarkup:
	kb = InlineKeyboardMarkup(row_width=1)
	kb.insert(InlineKeyboardButton(text='Да', callback_data='True'))
	kb.insert(InlineKeyboardButton(text='Нет', callback_data='False'))
	return kb


def get_edit_patient_kb() -> InlineKeyboardMarkup:
	kb = InlineKeyboardMarkup(row_width=1)
	kb.insert(InlineKeyboardButton(text='Добавить/удалить с ОПП', callback_data='edit_patient_is_opp'))
	kb.insert(InlineKeyboardButton(text='Добавить/удалить с Гепа-Мерц', callback_data='edit_patient_is_gepa_merz'))
	kb.insert(InlineKeyboardButton(text='Изменить дату поступления', callback_data='edit_patient_admission_date'))
	kb.insert(InlineKeyboardButton(text='Изменить дату выписки', callback_data='edit_patient_discharge_date'))
	kb.insert(InlineKeyboardButton(text='Удалить пациента', callback_data='delete_patient'))
	return kb


def get_edit_doctor_kb() -> InlineKeyboardMarkup:
	kb = InlineKeyboardMarkup(row_width=1)
	kb.insert(InlineKeyboardButton(text='Добавить/удалить с ОПП', callback_data='edit_doctor_access_opp'))
	kb.insert(InlineKeyboardButton(text='Добавить/удалить с Гепа-Мерц', callback_data='edit_doctor_access_gepa_merz'))
	return kb
