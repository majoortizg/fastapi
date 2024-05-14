from bson import ObjectId
from fastapi import HTTPException, APIRouter
from starlette.responses import JSONResponse
from db.db import collection_carrito, collection_users
from db.db import collection_carritodetalles
from db.db import collection_product
from model import usuario
from model.carrito import Carrito
from model.carritoDetalles import CarritoDetalles
from model.carritoRequest import CarritoRequest
from model.producto import Producto
import json


router = APIRouter()

@router.post("/", response_description= "Crear un nuevo carrito", response_model=Carrito)
async def create_carrito(carritoRequest: CarritoRequest):
    #existing_carrito = await collection_carrito.find_one([{"usuario": carritoRequest.usuario}, {"estado": "Pendiente"}])
    existing_carrito = await collection_carrito.find_one({"usuario": carritoRequest.usuario, "estado": "Pendiente"})
    # Si se encuentra un carrito pendiente para este usuario, lanzar una excepción
    if existing_carrito != None:
        raise HTTPException(status_code=400, detail="Ya existe un carrito pendiente para este usuario")
    existing_carrito = await collection_carrito.find_one([{"usuario": carritoRequest.usuario}])
    totalprecio = 0
    totalproductos = 0
    for request in carritoRequest.detalles:
        print(request)
        producto = await collection_product.find_one({"_id": ObjectId(request.idproducto)})
        print(producto)
        totalprecio += (producto ["precio"] * request.cantidadproductos)
        totalproductos += request.cantidadproductos
    carrito = {"usuario": carritoRequest.usuario, "estado": "Pendiente", "totalprecio": totalprecio, "totalproductos": totalproductos}
    result = await collection_carrito.insert_one(carrito)
    for detalle in carritoRequest.detalles:
        detalle.idcarrito = str(result.inserted_id)
        resultdetalle = await collection_carritodetalles.insert_one(detalle.dict())
    return carrito

@router.put("/{idCarrito}", response_model=Carrito)
async def update_carrito(idCarrito: str, carritoDetalles: list[CarritoDetalles]):
    carrito = await collection_carrito.find_one({"_id": ObjectId(idCarrito)})
    if carrito == None:
        raise HTTPException(status_code=400, detail="Carrito no encontrado")
    totalprecio = 0
    totalproductos = 0
    for request in carritoDetalles:
        producto = await collection_product.find_one({"_id": ObjectId(request.idproducto)})
        carritoDetalle = await collection_carritodetalles.find_one({"idproducto": request.idproducto})
        if carritoDetalle:
            carritoDetalle ["cantidadproductos"] = request.cantidadproductos
            carritoDetalle = await collection_carritodetalles.update_one({"_id": carritoDetalle.get("_id")}, {"$set": carritoDetalle})
        if carritoDetalle == None:
            request.idcarrito = str(idCarrito)
            resultdetalle = await collection_carritodetalles.insert_one(request.dict())
    existing_detalle = collection_carritodetalles.find({"idcarrito": str(carrito.get("_id"))})
    lista = []
    for detalle in await existing_detalle.to_list(100):
        producto = await collection_product.find_one({"_id": ObjectId(detalle["idproducto"])})
        totalprecio += (producto["precio"] * detalle["cantidadproductos"])
        totalproductos += detalle["cantidadproductos"]
        lista.append(detalle)
    carrito["productos"] = list(lista)
    carrito["id"] = str(carrito["_id"])
    carrito ["totalprecio"] = totalprecio
    carrito ["totalproductos"] = totalproductos
    carritoUpdate = await collection_carrito.update_one({"_id": ObjectId(idCarrito)}, {"$set": carrito})
    return carrito

@router.get("/{email}", response_model=Carrito)
async def find_carrito_by_email(email:str):
    #existing_carrito = await collection_carrito.find_one([{"usuario": email}, {"estado": "Pendiente"}])
    existing_carrito = await collection_carrito.find_one({"usuario": email, "estado": "Pendiente"})
    print(existing_carrito)
    if existing_carrito == None:
        raise HTTPException(status_code=400, detail="Carrito no existe")
    existing_detalle = collection_carritodetalles.find({"idcarrito": str(existing_carrito.get("_id"))})
    print(existing_detalle)
    lista = []
    for detalle in await existing_detalle.to_list(100):
        lista.append(detalle)
    existing_carrito["productos"] = list(lista)
    existing_carrito["id"] = str(existing_carrito["_id"])
    response = {"carrito": str(existing_carrito), "productos": str(lista)}
    return existing_carrito

#error 400
# #delete detalle de un producto, solo se borra producto

