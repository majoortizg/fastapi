from fastapi import HTTPException, APIRouter, Query
from bson import ObjectId
from db.db import collection_product
from model.producto import Producto

router = APIRouter()
@router.post("/producto nuevo", response_description= "Crear un nuevo producto", response_model=Producto)
async def create_producto(producto: Producto):
    existing_producto = await collection_product.find_one({"Nombre Producto": producto.nombreProd})
    if existing_producto != None:
        raise HTTPException(status_code=404, detail="El producto ya existe")
    result = await collection_product.insert_one(producto.dict())
    producto._id = str(result.inserted_id)
    return producto

@router.get("/productos", response_description="Listar productos", response_model=list[Producto])
async def read_productos():
    productos = await collection_product.find().to_list(100)
    for producto in productos:
        producto["id"] = str(producto["_id"])
        print(producto)
    return productos

@router.get("/categoria", response_description="Listar productos por categoría", response_model=list[Producto])
async def read_productos_categoria(categoria: str = Query(None)):
    if categoria is None:
        raise HTTPException(status_code=400, detail="Se requiere especificar una categoría para listar productos.")
    productos = await collection_product.find({"categoria": categoria}).to_list(100)
    for producto in productos:
        producto["id"] = str(producto["_id"])
    return productos

@router.get("/{id_producto}", response_model=Producto)
async def find_producto_by_id(id_producto:str):
    producto = await collection_product.find_one({"_id": ObjectId(id_producto)})
    if producto:
        producto["id"] = str(producto["_id"])
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.put("/{ID producto}", response_model=Producto)
async def update_producto(_id: str, producto: Producto):
    updated:producto = await collection_product.find_one_and_update({"_id": ObjectId(_id)}, {"$set": producto.dict()})
    if update_producto:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/{ID producto}", response_model=Producto)
async def delete_producto(_id:str):
    deleted_producto = await collection_product.find_one_and_delete({"_id": ObjectId(_id)})
    if deleted_producto:
        return deleted_producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")




