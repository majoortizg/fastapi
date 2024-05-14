from bson import ObjectId
from fastapi import HTTPException, APIRouter
from db.db import collection_tarjetas
from db.db import collection_carrito
from model.tarjetas import Tarjetas
from model.compra import Compra
from model.carrito import Carrito

router = APIRouter()

@router.post("/tarjetas", response_description= "crear un nueva tarjeta", response_model=Tarjetas)
async def create_tarjeta(tarjeta: Tarjetas):
    existing_tarjeta = await collection_tarjetas.find_one({"numero tarjeta": tarjeta.numeroTarjeta})
    if existing_tarjeta != None:
        raise HTTPException(status_code=404, detail="Tarjeta ya existe")
    result = await collection_tarjetas.insert_one(tarjeta.dict())
    tarjeta._id = str(result.inserted_id)
    return tarjeta


@router.get("/tarjetas", response_description="Listar tarjetas", response_model=list[Tarjetas])
async def read_tarjetas():
    tarjetas = await collection_tarjetas.find().to_list(100)

    for tarjeta in tarjetas:
        tarjeta["_id"] = str(tarjeta["_id"])
        print(tarjeta)
    return tarjetas

#@router.post("/pago", response_description= "Metodo de Pago")
#async def pago_tarjeta(tarjeta: Tarjetas):
#    existing_tarjeta = await collection_tarjetas.find_one({"numeroTarjeta": tarjeta.numeroTarjeta})
#    if existing_tarjeta == None:
#        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
#    if existing_tarjeta["fechaCaducidad"] != tarjeta.fechaCaducidad:
#        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
#    if existing_tarjeta["cvv"] != tarjeta.cvv:
#        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
#    tarjetaValida = ("Tarjeta valida. \n Compra exitosa.")
#    return tarjetaValida

@router.post("/realizarCompra", response_description= "Metodo de Pago")
async def realizar_compra(compra: Compra):
    existing_tarjeta = await collection_tarjetas.find_one({"numeroTarjeta": compra.tarjeta.numeroTarjeta})
    if existing_tarjeta == None:
        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
    if existing_tarjeta["fechaCaducidad"] != compra.tarjeta.fechaCaducidad:
        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
    if existing_tarjeta["cvv"] != compra.tarjeta.cvv:
        raise HTTPException(status_code=404, detail="Tarjeta invalida.")
    existing_carrito = await collection_carrito.find_one({"_id": ObjectId(compra.idcarrito)})
    if existing_carrito == None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    if existing_carrito["totalprecio"] >= existing_tarjeta["saldo"]:
        raise HTTPException(status_code=404, detail="Compra no exitosa. (Fondos insuficientes)")
    existing_carrito["estado"] = "Carrito comprado."
    existing_tarjeta["saldo"] = existing_tarjeta["saldo"] - existing_carrito["totalprecio"]
    updated: existing_carrito = await collection_carrito.update_one({"_id": ObjectId(compra.idcarrito)}, {"$set": existing_carrito})
    updated: existing_tarjeta = await collection_tarjetas.update_one({"numeroTarjeta": compra.tarjeta.numeroTarjeta}, {"$set": existing_tarjeta})
    tarjetaValida = ("Compra exitosa.")
    return tarjetaValida
