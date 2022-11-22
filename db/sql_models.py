from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine


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


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)
