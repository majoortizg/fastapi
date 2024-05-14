import certifi #trae el paquete completo
from motor.motor_asyncio import AsyncIOMotorClient #trae una parte del paquete
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URL= os.environ.get("MONGO_DB")
client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
database = client["ing_swii"]
collection_users = database["users"]
collection_product = database["product"]
collection_carrito = database["carrito"]
collection_carritodetalles = database["carritodetalles"]
collection_tarjetas = database["tarjetas"]
