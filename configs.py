from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    CON_STR: str = "postgresql://postgres:admin@localhost/igara"
    DBBaseModel = declarative_base()


settings = Settings()