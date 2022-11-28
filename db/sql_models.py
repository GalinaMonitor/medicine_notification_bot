import re
from datetime import date
from typing import Optional

from pydantic import validator
from sqlalchemy import Column, BigInteger, Text
from sqlmodel import SQLModel, Field, create_engine

from config import settings


class Doctor(SQLModel, table=True):
	id: Optional[int] = Field(
		sa_column=Column(BigInteger(), default=None, primary_key=True)
	)
	fullname: str
	access_opp: Optional[bool] = Field(default=True)
	access_gepa_merz: Optional[bool] = Field(default=False)


class Patient(SQLModel, table=True):
	history_number: Optional[str] = Field(
		sa_column=Column(Text(), default=None, primary_key=True)
	)
	fullname: str
	admission_date: Optional[date] = Field(default=None)
	discharge_date: Optional[date] = Field(default=None)
	is_opp: bool
	is_gepa_merz: bool

	@validator('history_number')
	def history_number_validation(cls, v):
		if not re.search('^[0-9]+-[0-9]{4}$', v):
			raise ValueError('Wrong history number')
		return v


engine = create_engine(settings.db_conn_string, echo=True)
SQLModel.metadata.create_all(engine)
