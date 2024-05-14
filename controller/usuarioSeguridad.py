from fastapi import HTTPException, APIRouter
from db.db import collection_users
from model.login import Login
from model.login_Reponse import LoginResponse
import jwt


router = APIRouter()
@router.post("/login", response_description= "Inicio de sesion")
async def login_usuario(login: Login):
    existing_user = await collection_users.find_one({"email": login.email})
    if existing_user == None:
        raise HTTPException(status_code=404, detail="Usuario o contraseña no existe.")
    if existing_user["password"] != login.password:
        raise HTTPException(status_code=404, detail="Usuario o contraseña no existe.")
    login_jwt = jwt.encode({"usuario": existing_user["email"]}, "secreto", algorithm= "HS256")
    return "token:" + login_jwt

#decode>>>> jwt.decode(token, "secreto", algorithms = ["HS256"])
#desxargar estas librerias y luego en Uage basic usage
#https://indominusbyte.github.io/fastapi-jwt-auth/
