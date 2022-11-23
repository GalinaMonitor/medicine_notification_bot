from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot import dp, bot, EditDoctorStatesGroup
from db.services.patients import DoctorService
from db.sql_models import Doctor
from keyboards.keyboard import get_edit_doctor_kb, get_cancel_kb


def get_doctor_info(doctor: Doctor):
	return f'''
	ФИО: {doctor.fullname}
	Доступ к ОПП: {'Да' if doctor.access_opp else 'Нет'}
	Доступ к Гепа-мерц: {'Да' if doctor.access_gepa_merz else 'Нет'}

	Чтобы вернуться в главное меню, нажмите /cancel
	'''


@dp.message_handler(lambda message: message.text == 'Редактировать профиль', state=None)
async def get_doctor(message: types.Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		data['id'] = int(message.from_user.id)
	doctor = DoctorService.get_doctor(telegram_id=message.from_user.id)
	await EditDoctorStatesGroup.edit.set()
	await message.answer(
		get_doctor_info(doctor),
		reply_markup=get_cancel_kb()
	)
	await message.answer(
		'Настроить доступ к исследованиям',
		reply_markup=get_edit_doctor_kb()
	)


@dp.callback_query_handler(lambda call: 'edit_doctor_' in call.data, state=EditDoctorStatesGroup.edit)
async def edit_doctor(callback_query: CallbackQuery, state: FSMContext):
	param = callback_query.data.replace('edit_doctor_', '')

	async with state.proxy() as data:
		doctor = DoctorService.get_doctor(telegram_id=data['id'])

	if param == 'access_opp':
		doctor = DoctorService.update_doctor(data['id'], access_opp=not doctor.access_gepa_merz)
	elif param == 'access_gepa_merz':
		doctor = DoctorService.update_doctor(data['id'], access_gepa_merz=not doctor.access_gepa_merz)

	await bot.send_message(callback_query.message.chat.id, 'Изменения внесены')
	await bot.send_message(
		callback_query.message.chat.id,
		get_doctor_info(doctor),
		reply_markup=get_edit_doctor_kb()
	)
