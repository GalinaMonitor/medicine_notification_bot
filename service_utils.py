from datetime import timedelta, date
from typing import List

from db.sql_models import Patient


def check_notifications_opp(patient: Patient, checked_date: date) -> List[str]:
	notification_list = []

	if patient.is_opp:
		if checked_date - patient.admission_date == timedelta(days=1):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - ОПП.Повторные анализы'
			)
		if checked_date - patient.admission_date == timedelta(days=5):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - ОПП.Повторные анализы'
			)
		if checked_date - patient.discharge_date == timedelta(weeks=12):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - ОПП.Повторный визит'
			)

	if not patient.is_opp:
		if checked_date - patient.admission_date == timedelta(days=7):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - БЕЗ ОПП.Повторные анализы'
			)
		if checked_date - patient.discharge_date == timedelta(days=12):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - БЕЗ ОПП.Повторный визит'
			)

	return notification_list


def check_notifications_gepa_merz(patient: Patient, checked_date: date) -> List[str]:
	notification_list = []

	if patient.is_gepa_merz:
		if checked_date - patient.admission_date == timedelta(weeks=4):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - Гепа-мерц.Повторный визит'
			)
		if checked_date - patient.discharge_date == timedelta(weeks=10):
			notification_list.append(
				f'{checked_date.strftime("%d-%m-%y")}: {patient.history_number} {patient.fullname} - Гепа-мерц.Повторный визит'
			)

	return notification_list
