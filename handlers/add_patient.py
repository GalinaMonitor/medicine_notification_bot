from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar
from aiogram_calendar.simple_calendar import calendar_callback

from bot import dp, NewPatientStatesGroup, bot
from db.exceptions import NotFoundException
from db.services.patients import PatientService
from db.sql_models import Patient
from keyboards.keyboard import get_cancel_kb, get_intro_kb, get_true_or_false


@dp.message_handler(lambda message: message.text == "Добавить пациента", state=None)
async def subscriptions_info(message: types.Message):
	await message.answer(
		'''
		Для регистрации пациента нужны следующие данные:
		- Номер истории болезни
		- ФИО
		- День поступления
		- День выписки
		- ОПП
		- Гепа-мерц
		Для отмены операции нажмите кнопку /cancel в скрытом меню
		''',
		reply_markup=get_cancel_kb()
	)
	await message.answer('Введите ФИО')
	await NewPatientStatesGroup.fullname.set()


@dp.message_handler(state=NewPatientStatesGroup.fullname)
async def load_fullname(message: types.Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		data['fullname'] = message.text

	await message.answer('Введите номер истории болезни')
	await NewPatientStatesGroup.next()


@dp.message_handler(state=NewPatientStatesGroup.history_number)
async def load_history_number(message: types.Message, state: FSMContext) -> None:
	try:
		Patient.history_number_validation(message.text)
	except ValueError:
		await message.answer('Номер должен соответствовать формату "номер-год". Введите другой номер истории болезни')
		return
	try:
		PatientService.get_patient(message.text)
	except NotFoundException:
		async with state.proxy() as data:
			data['history_number'] = message.text

		await message.answer('Введите дату поступления пациента', reply_markup=await SimpleCalendar().start_calendar())
		await NewPatientStatesGroup.next()
		return

	await message.answer('Пациент с этим номером в базе уже есть. Введите другой номер истории болезни')


@dp.callback_query_handler(calendar_callback.filter(), state=NewPatientStatesGroup.admission_date)
async def load_admission_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
	selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
	if selected:
		await callback_query.message.answer(
			f'Вы ввели {date.strftime("%d/%m/%Y")}'
		)
		async with state.proxy() as data:
			data['admission_date'] = date
		await callback_query.message.answer(
			f'Пациент уже выписался?',
			reply_markup=get_true_or_false()
		)
		await NewPatientStatesGroup.next()


@dp.callback_query_handler(lambda call: call.data in ['True', 'False'], state=NewPatientStatesGroup.discharge_date)
async def is_discharge_date(callback_query: CallbackQuery):
	if callback_query.data == 'True':
		await callback_query.message.answer(
			f'Введите дату выписки пациента',
			reply_markup=await SimpleCalendar().start_calendar()
		)
	else:
		await NewPatientStatesGroup.next()
		await callback_query.message.answer(
			f'Пациент с ОПП?', reply_markup=get_true_or_false()
		)


@dp.callback_query_handler(calendar_callback.filter(), state=NewPatientStatesGroup.discharge_date)
async def load_discharge_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
	selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
	if selected:
		await callback_query.message.answer(
			f'Вы ввели {date.strftime("%d/%m/%Y")}'
		)
		async with state.proxy() as data:
			data['discharge_date'] = date
		await callback_query.message.answer(
			f'Пациент с ОПП?', reply_markup=get_true_or_false()
		)
		await NewPatientStatesGroup.next()


@dp.callback_query_handler(lambda call: call.data in ['True', 'False'], state=NewPatientStatesGroup.is_opp)
async def load_is_oop(callback_query: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['is_opp'] = True if callback_query.data == 'True' else False
	await callback_query.message.answer(
		f'Пациент с + гепа-мерц?', reply_markup=get_true_or_false()
	)
	await NewPatientStatesGroup.next()


@dp.callback_query_handler(lambda call: call.data in ['True', 'False'], state=NewPatientStatesGroup.is_gepa_merz)
async def load_is_gepa_merz(callback_query: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['is_gepa_merz'] = True if callback_query.data == 'True' else False
		PatientService.create_patient(**data)
	await bot.send_message(callback_query.message.chat.id, 'Пациент добавлен', reply_markup=get_intro_kb())
	await state.finish()
