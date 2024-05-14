from typing import Optional
from pydantic import BaseModel
from db.db import collection_product
from bson import ObjectId

class Producto(BaseModel):
    id: Optional[str]
    nombreProd: str
    marca: str
    categoria: str
    precio: float

