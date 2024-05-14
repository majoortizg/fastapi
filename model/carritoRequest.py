from pydantic import BaseModel
from model.carritoDetalles import CarritoDetalles

class CarritoRequest(BaseModel):
    usuario: str
    detalles: list[CarritoDetalles]