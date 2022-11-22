from sqlmodel import SQLModel


class Error(SQLModel):
	code: int
	message: str


class NotFoundException(Exception):
	def __init__(self):
		self.body = Error(code=404, message='Item not found').dict()
