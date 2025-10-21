from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import EventoSchema
from services.CancelacionServices import CancelacionServices
from services.InutilizacionServices import InutilizacionServices

router = APIRouter(prefix="/SifenConect/evento", tags=["Eventos"])

@router.post("/cancelacion")
def post_cancelacion(evento: EventoSchema, db: Session = Depends(get_db)):
    return CancelacionServices(db).cancelacion(evento)

@router.post("/inutilizacion")
def post_inutilizacion(evento: EventoSchema, db: Session = Depends(get_db)):
    return InutilizacionServices(db).inutilizacion(evento)
