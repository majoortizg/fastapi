from typing import Optional

from pydantic import BaseModel
from model.carritoDetalles import CarritoDetalles


class Carrito(BaseModel):
    id: Optional[str]
    usuario: str
    estado: str
    totalprecio: float
    totalproductos: int
    productos: Optional[list[CarritoDetalles]]