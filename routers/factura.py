from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import FacturaSchema
from services.FacturaServices import FacturaService

router = APIRouter(prefix="/SifenConect", tags=["Factura"])

@router.post("/FE")
def post_factura_electronica(factura: FacturaSchema, db: Session = Depends(get_db)):
    return FacturaService(db).postFacturaElectronica(factura)

@router.post("/NC")
def post_nota_credito(factura: FacturaSchema, db: Session = Depends(get_db)):
    return FacturaService(db).postNotaCredito(factura)
