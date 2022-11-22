from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine

from config import settings


class Doctor(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	fullname: str
	access_opp: Optional[bool] = Field(default=True)
	access_gepa_merz: Optional[bool] = Field(default=False)


class Patient(SQLModel, table=True):
	history_number: Optional[int] = Field(default=None, primary_key=True)
	fullname: str
	admission_date: Optional[date] = Field(default=None)
	discharge_date: Optional[date] = Field(default=None)
	is_opp: bool
	is_gepa_merz: bool


engine = create_engine(settings.db_conn_string, echo=True)
SQLModel.metadata.create_all(engine)
