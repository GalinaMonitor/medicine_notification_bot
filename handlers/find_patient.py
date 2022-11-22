from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp, FindPatientStatesGroup
from db.exceptions import NotFoundException
from db.services.patients import PatientService
from keyboards.keyboard import get_cancel_kb, get_intro_kb


@dp.message_handler(lambda message: message.text == 'Найти пациента по номеру истории болезни')
async def find_patient_answer(message: types.Message):
	await FindPatientStatesGroup.question.set()
	await message.reply(
		'Введите номер истории болезни',
		reply_markup=get_cancel_kb()
	)


@dp.message_handler(lambda message: not message.text.isdigit(), state=FindPatientStatesGroup.question)
async def check_history_number(message: types.Message):
	await message.reply('Введите правильный номер истории болезни')


@dp.message_handler(state=FindPatientStatesGroup.question)
async def find_patient(message: types.Message, state: FSMContext) -> None:
	try:
		patient = PatientService.get_patient(history_number=int(message.text))
		await message.answer(
			f'''
			Номер истории болезни: {patient.history_number}
			ФИО: {patient.fullname}
			День поступления: {patient.admission_date}
			День выписки: {patient.discharge_date}
			ОПП: {'Да' if patient.is_opp else 'Нет'}
			Гепа-мерц: {'Да' if patient.is_gepa_merz else 'Нет'}
			'''
			, reply_markup=get_intro_kb()
		)
		await state.finish()
	except NotFoundException:
		await message.answer('Номер не найден. Попробуйте еще раз')
