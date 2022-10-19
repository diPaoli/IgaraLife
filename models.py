from sqlalchemy import Column, Integer, Float, Date

from configs import settings
from schemas import LeituraSchema



class LeituraModel(settings.DBBaseModel):
    __tablename__ = 'leituras'

    id = Column(Integer, primary_key=True)
    apartamento = Column(Integer)
    gas = Column(Float)
    agua = Column(Float)
    data = Column(Date)

    class Config:
        orm_mode = True

    @classmethod
    def create_from_schema(self, leitura_body: LeituraSchema):
        return self(**dict(leitura_body))
        
