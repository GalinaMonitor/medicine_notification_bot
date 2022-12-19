import os
from datetime import datetime

import openpyxl as openpyxl
from aiogram import types
from aiogram.types import InputFile

from bot import dp
from db.services.patients import PatientService


@dp.message_handler(lambda message: message.text == "Получить excel-файл", state=None)
async def get_excel(message: types.Message):
	patients = PatientService.get_patients()
	wb = openpyxl.Workbook()
	sheet = wb.active
	sheet.column_dimensions['B'].width = 20
	sheet.column_dimensions['C'].width = 20
	sheet.column_dimensions['D'].width = 20
	sheet.append(('Номер', 'ФИО', 'Дата поступления', 'Дата выписки', 'ОПП', 'Гепа-мерц'))
	for patient in patients:
		sheet.append(
			(
				patient.history_number,
				patient.fullname,
				patient.admission_date,
				patient.discharge_date if patient.discharge_date else 'Не выписан',
				'Да' if patient.is_opp else 'Нет',
				'Да' if patient.is_gepa_merz else 'Нет',
			)
		)
	if not os.path.isdir('./temp'):
		os.mkdir('./temp')
	filename = f'./temp/patient_list_{datetime.now().strftime("%d-%m-%y")}.xlsx'
	wb.save(filename)
	await message.answer_document(InputFile(filename))
	os.remove(filename)
