from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel, NotaCreditoDebito as NotaCreditoDebitoModel,Evento as EventoModel,Operacion as OperacionModel,Estado as EstadoModel
from schemas import FacturaSchema , EventoSchema
from services.FacturaServices import FacturaService
from services.ConsultaServices import ConsultaServices
from services.CancelacionServices import CancelacionServices
from services.InutilizacionServices import InutilizacionServices

app = FastAPI()

@app.post("/Api/sifen/FE")
def postFE(factura: FacturaSchema, db: Session = Depends(get_db)):
    return FacturaService(db).postFacturaElectronica(factura)

@app.post("/Api/sifen/NC")
def postNC(factura: FacturaSchema, db: Session = Depends(get_db)):
    return FacturaService(db).postNotaCredito(factura)
    


@app.post("/Api/sifen/evento/cancelacion")
def postCancelacion(evento: EventoSchema, db: Session = Depends(get_db)):
    return CancelacionServices(db).cancelacion(evento)
    
    
@app.post("/Api/sifen/evento/inutilizacion")
def postInutilizacion(evento: EventoSchema, db: Session = Depends(get_db)):
    return InutilizacionServices(db).inutilizacion(evento)


@app.get("/Api/sifen/consulta/{cdc}")
def consultar_estado_cdc(cdc: str, db: Session = Depends(get_db)):
    return ConsultaServices(db).consulta(cdc)