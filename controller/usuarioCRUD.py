from fastapi import HTTPException, APIRouter
from db.db import collection_users
from model.usuario import Usuario

router = APIRouter()
@router.post("/", response_description= "crear un nuevo usuario", response_model=Usuario)
async def create_usuario(usuario: Usuario):
    existing_user = await collection_users.find_one({"email": usuario.email})
    if existing_user != None:
        raise HTTPException(status_code=404, detail="Email ya existe")
    if "@" not in usuario.email:
        raise HTTPException(status_code=400, detail="El email debe contener un '@'")
    min_length_password = 8
    if len(usuario.password) < min_length_password:
        raise HTTPException(status_code=400, detail=f"La contraseña debe tener al menos {min_length_password} caracteres")
    if not any(char.isupper() for char in usuario.password) or not any(char.isdigit() for char in usuario.password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener al menos una letra mayúscula y un número")
    result = await collection_users.insert_one(usuario.dict())
    usuario._id = str(result.inserted_id)
    return usuario

@router.get("/", response_description="Listar usuarios", response_model=list[Usuario])
async def read_usuarios():
    usuarios = await collection_users.find().to_list(100)
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])
        print(usuario)
    return usuarios

@router.get("/{email}", response_model=Usuario)
async def find_usuario_by_email(email:str):
    usuario = await collection_users.find_one({"email": email})
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="usuario no encontrado")

@router.put("/{email", response_model=Usuario)
async def update_usuario(email: str, usuario: Usuario):
    updated:usuario = await collection_users.find_one_and_update({"email": email}, {"$set": usuario.dict()})
    if update_usuario:
        return usuario
    raise HTTPException(status_code=404, detail="usuario no encontrado")

@router.delete("/{email}", response_model=Usuario)
async def delete_usuario(email:str):
    deleted_usuario = await collection_users.find_one_and_delete({"email": email})
    if deleted_usuario:
        return deleted_usuario
    raise HTTPException(status_code=404, detail="usuario no encontrado")


