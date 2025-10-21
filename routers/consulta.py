from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ConsultaServices import ConsultaServices

router = APIRouter(prefix="/SifenConect", tags=["Consulta"])

@router.get("/consulta/{cdc}")
def get_consulta(cdc: str, db: Session = Depends(get_db)):
    return ConsultaServices(db).consulta(cdc)
