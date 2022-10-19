from sqlalchemy import create_engine
from configs import settings


engine = create_engine(settings.CON_STR)
