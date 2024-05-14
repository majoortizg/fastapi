from pydantic import BaseModel

class Tarjetas(BaseModel):
    numeroTarjeta: str
    fechaCaducidad: str
    cvv: str
    titular: str
    saldo: float