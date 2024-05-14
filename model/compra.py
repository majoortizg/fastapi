from pydantic import BaseModel
from model.tarjetas import Tarjetas

class Compra(BaseModel):
    tarjeta: Tarjetas
    idcarrito: str