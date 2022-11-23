from datetime import datetime, timedelta

from aiogram import types

from bot import dp
from db.exceptions import NotFoundException
from db.services.patients import DoctorService, PatientService
from keyboards.keyboard import get_intro_kb
from service_utils import check_notifications_opp, check_notifications_gepa_merz


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
	try:
		doctor = DoctorService.get_doctor(message.from_user.id)
	except NotFoundException:
		DoctorService.create_doctor(id=message.from_user.id, fullname=message.from_user.full_name)
		doctor = DoctorService.get_doctor(message.from_user.id)
	await message.answer(
		f'Здравствуйте, {doctor.fullname}',
		reply_markup=get_intro_kb()
	)
	await message.delete()


@dp.message_handler(lambda message: message.text == "Напоминания на сегодня")
async def notification_info(message: types.Message):
	today = datetime.now().date()
	opp_notification_list = []
	gepa_merz_notification_list = []

	for patient in PatientService.get_patients():
		if patient.is_opp:
			opp_notification_list += check_notifications_opp(patient, today)

			if today.weekday() == 4:
				opp_notification_list += check_notifications_opp(patient, today + timedelta(days=1))
				opp_notification_list += check_notifications_opp(patient, today + timedelta(days=2))

		if patient.is_gepa_merz:
			gepa_merz_notification_list += check_notifications_gepa_merz(patient, today)

			if today.weekday() == 4:
				gepa_merz_notification_list += check_notifications_gepa_merz(patient, today + timedelta(days=1))
				gepa_merz_notification_list += check_notifications_gepa_merz(patient, today + timedelta(days=2))

	for doctor in DoctorService.get_doctors():
		if doctor.access_opp and len(opp_notification_list):
			await message.reply(
				'\n'.join(opp_notification_list)
			)
		if doctor.access_gepa_merz and len(gepa_merz_notification_list):
			await message.reply(
				'\n'.join(gepa_merz_notification_list)
			)
		if not len(opp_notification_list) and not len(gepa_merz_notification_list):
			await message.reply(
				'Напоминаний на сегодня нет'
			)
