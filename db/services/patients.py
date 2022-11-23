from typing import List

from sqlmodel import select, Session

from db.exceptions import NotFoundException
from db.sql_models import engine, Patient, Doctor


class DoctorService:
	@staticmethod
	def create_doctor(**args):
		with Session(engine) as session:
			doctor = Doctor(**args)
			session.add(doctor)
			session.commit()
			return doctor

	@staticmethod
	def update_doctor(telegram_id: int, **args):
		with Session(engine) as session:
			statement = select(Doctor).where(Doctor.id == telegram_id)
			doctor = session.exec(statement).first()
			if not doctor:
				raise NotFoundException()

			for key, value in args.items():
				setattr(doctor, key, value)
			session.add(doctor)
			session.commit()
			session.refresh(doctor)
			return doctor

	@staticmethod
	def get_doctor(telegram_id: int) -> Doctor:
		with Session(engine) as session:
			statement = select(Doctor).where(Doctor.id == telegram_id)
			doctor = session.exec(statement).first()
			if not doctor:
				raise NotFoundException()

			return doctor

	@staticmethod
	def get_doctors() -> List[Doctor]:
		with Session(engine) as session:
			statement = select(Doctor)
			doctors = session.exec(statement).all()
			return doctors


class PatientService:
	@staticmethod
	def create_patient(**args):
		with Session(engine) as session:
			patient = Patient(**args)
			session.add(patient)
			session.commit()
			session.refresh(patient)
			return patient

	@staticmethod
	def update_patient(history_number: int, **args):
		with Session(engine) as session:
			statement = select(Patient).where(Patient.history_number == history_number)
			patient = session.exec(statement).first()
			if not patient:
				raise NotFoundException()

			for key, value in args.items():
				setattr(patient, key, value)
			session.add(patient)
			session.commit()
			session.refresh(patient)
			return patient

	@staticmethod
	def delete_patient(history_number: int):
		with Session(engine) as session:
			statement = select(Patient).where(Patient.history_number == history_number)
			patient = session.exec(statement).first()
			if not patient:
				raise NotFoundException()

			session.delete(patient)
			session.commit()

	@staticmethod
	def get_patient(history_number: int) -> Patient:
		with Session(engine) as session:
			statement = select(Patient).where(Patient.history_number == history_number)
			patient = session.exec(statement).first()
			if not patient:
				raise NotFoundException()

			return patient

	@staticmethod
	def get_patients() -> List[Patient]:
		with Session(engine) as session:
			statement = select(Patient)
			patients = session.exec(statement).all()
			return patients
