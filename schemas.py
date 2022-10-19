from datetime import date
from typing import Optional
from pydantic import BaseModel


class LeituraSchema(BaseModel):
    id: Optional[int]
    apartamento: Optional[int]
    gas: Optional[float]
    agua: Optional[float]
    data: Optional[date]
