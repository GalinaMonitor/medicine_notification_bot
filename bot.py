from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import settings

storage = MemoryStorage()
bot = Bot(settings.bot_token)
dp = Dispatcher(bot, storage=storage)


class NewPatientStatesGroup(StatesGroup):
	fullname = State()
	history_number = State()
	admission_date = State()
	discharge_date = State()
	is_opp = State()
	is_gepa_merz = State()


class EditPatientStatesGroup(StatesGroup):
	request = State()
	result = State()
	edit = State()
	admission_date = State()
	discharge_date = State()


class EditDoctorStatesGroup(StatesGroup):
	edit = State()


if __name__ == '__main__':
	from handlers.intro import *
	from handlers.add_patient import *
	from handlers.edit_patient import *
	from handlers.edit_doctor import *
	from handlers.create_excel import *

	executor.start_polling(dp, skip_updates=True)
