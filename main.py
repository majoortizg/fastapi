from fastapi import FastAPI, HTTPException
from db.db import client
from controller.usuarioCRUD import router as usuarios_router
from controller.productoCRUD import router as productos_router
from controller.usuarioSeguridad import router as seguridad_router
from controller.carritoCompras import router as carrito_router
from controller.tarjetasPago import router as tarjetas_router

app = FastAPI()

app.include_router(seguridad_router, tags=["Login"], prefix="/login")
app.include_router(usuarios_router, tags=["Usuarios"], prefix="/usuarios")
app.include_router(productos_router, tags=["Productos"], prefix="/productos")
app.include_router(carrito_router, tags=["Carrito compras"], prefix="/carrito")
app.include_router(tarjetas_router, tags=["Metodo de pago"], prefix="/tarjetas pago")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()



