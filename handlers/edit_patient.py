from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar.simple_calendar import calendar_callback, SimpleCalendar

from bot import dp, EditPatientStatesGroup, bot
from db.exceptions import NotFoundException
from db.services.patients import PatientService
from db.sql_models import Patient
from keyboards.keyboard import get_cancel_kb, get_intro_kb, get_edit_patient_kb


def get_patient_info(patient: Patient):
	return f'''
	Номер истории болезни: {patient.history_number}
	ФИО: {patient.fullname}
	День поступления: {patient.admission_date}
	День выписки: {patient.discharge_date}
	ОПП: {'Да' if patient.is_opp else 'Нет'}
	Гепа-мерц: {'Да' if patient.is_gepa_merz else 'Нет'}
	
	Чтобы вернуться в главное меню, нажмите /cancel
	'''


@dp.message_handler(lambda message: message.text == 'Найти пациента по номеру истории болезни', state=None)
async def find_patient_answer(message: types.Message):
	await EditPatientStatesGroup.request.set()
	await message.reply(
		'Введите номер истории болезни',
		reply_markup=get_cancel_kb()
	)


@dp.message_handler(lambda message: not message.text.isdigit(), state=EditPatientStatesGroup.request)
async def check_history_number(message: types.Message):
	await message.reply('Введите правильный номер истории болезни')


@dp.message_handler(state=EditPatientStatesGroup.request)
async def find_patient(message: types.Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		data['history_number'] = int(message.text)
	try:
		patient = PatientService.get_patient(history_number=int(message.text))
		await message.answer(
			get_patient_info(patient),
			reply_markup=get_edit_patient_kb()
		)
		await EditPatientStatesGroup.result.set()
	except NotFoundException:
		await message.answer('Номер не найден. Попробуйте еще раз')


@dp.callback_query_handler(lambda call: call.data == 'delete_patient', state=EditPatientStatesGroup.result)
async def delete_patient(callback_query: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		PatientService.delete_patient(history_number=data['history_number'])
	await state.finish()
	await bot.send_message(
		callback_query.message.chat.id,
		f'Пациент удален',
		reply_markup=get_intro_kb()
	)


@dp.callback_query_handler(lambda call: 'edit_patient_' in call.data, state=EditPatientStatesGroup.result)
async def edit_patient(callback_query: CallbackQuery, state: FSMContext):
	param = callback_query.data.replace('edit_patient_', '')

	async with state.proxy() as data:
		patient = PatientService.get_patient(history_number=data['history_number'])

	if param == 'is_opp':
		patient = PatientService.update_patient(data['history_number'], is_opp=not patient.is_opp)
	elif param == 'is_gepa_merz':
		patient = PatientService.update_patient(data['history_number'], is_gepa_merz=not patient.is_gepa_merz)

	elif param == 'admission_date':
		await EditPatientStatesGroup.admission_date.set()
		await bot.send_message(
			callback_query.message.chat.id,
			f'Введите дату поступления',
			reply_markup=await SimpleCalendar().start_calendar()
		)
		return

	elif param == 'discharge_date':
		await EditPatientStatesGroup.discharge_date.set()
		await bot.send_message(
			callback_query.message.chat.id,
			f'Введите дату выписки',
			reply_markup=await SimpleCalendar().start_calendar()
		)
		return

	await bot.send_message(callback_query.message.chat.id, 'Изменения внесены')
	await bot.send_message(
		callback_query.message.chat.id,
		get_patient_info(patient),
		reply_markup=get_edit_patient_kb()
	)


@dp.callback_query_handler(calendar_callback.filter(), state=EditPatientStatesGroup.admission_date)
async def load_admission_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
	selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
	if selected:
		await callback_query.message.answer(
			f'Вы ввели {date.strftime("%d/%m/%Y")}'
		)
		async with state.proxy() as data:
			patient = PatientService.update_patient(data['history_number'], admission_date=date)
		await EditPatientStatesGroup.result.set()
		await bot.send_message(callback_query.message.chat.id, 'Изменения внесены')
		await bot.send_message(
			callback_query.message.chat.id,
			get_patient_info(patient),
			reply_markup=get_edit_patient_kb()
		)


@dp.callback_query_handler(calendar_callback.filter(), state=EditPatientStatesGroup.discharge_date)
async def load_discharge_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
	selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
	if selected:
		await callback_query.message.answer(
			f'Вы ввели {date.strftime("%d/%m/%Y")}'
		)
		async with state.proxy() as data:
			patient = PatientService.update_patient(data['history_number'], discharge_date=date)
		await EditPatientStatesGroup.result.set()
		await bot.send_message(callback_query.message.chat.id, 'Изменения внесены')
		await bot.send_message(
			callback_query.message.chat.id,
			get_patient_info(patient),
			reply_markup=get_edit_patient_kb()
		)
