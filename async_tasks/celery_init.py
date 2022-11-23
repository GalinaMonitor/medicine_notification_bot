import asyncio
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab

from bot import bot
from config import settings
from db.services.patients import PatientService, DoctorService
from service_utils import check_notifications_opp, check_notifications_gepa_merz

celery_app = Celery(
	broker=settings.redis_url,
	redis_max_connections=3,
	result_persistent=True,
	enable_ut=True,
	timezone="Europe/Moscow",
	redis_socket_timeout=15,
	event_serializer='json',
	task_serializer='json',
	acks_late=True,
	prefetch_multiplier=1,
	create_missing_queues=True,
)


@celery_app.task
def send_notification():
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
			asyncio.run(bot.send_message(
				doctor.id,
				'\n'.join(opp_notification_list)
			))
		if doctor.access_gepa_merz and len(gepa_merz_notification_list):
			asyncio.run(bot.send_message(
				doctor.id,
				'\n'.join(gepa_merz_notification_list)
			))


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(
		crontab(
			hour='14',
			minute='0',
			day_of_week='1-5'
		),
		send_notification,
	)
