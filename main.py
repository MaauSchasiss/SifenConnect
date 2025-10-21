from fastapi import FastAPI
from routers import factura, eventos, consulta

app = FastAPI(title="Sifen API", version="2.0")

# Registrar routers
app.include_router(factura.router)
app.include_router(eventos.router)
app.include_router(consulta.router)