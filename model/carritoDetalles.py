from pydantic import BaseModel


class CarritoDetalles(BaseModel):
    idcarrito: str
    idproducto: str
    cantidadproductos: int
