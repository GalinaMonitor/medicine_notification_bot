from pydantic import BaseSettings


class Settings(BaseSettings):
	redis_url: str = 'redis://localhost:6379/0'
	bot_token: str
	db_conn_string: str


settings = Settings()
