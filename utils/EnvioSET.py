from fastapi import Depends, HTTPException
from database import get_db
from schemas import FacturaSchema
from sqlalchemy.orm import Session
from models import Documento


def envioAlaSET(factura: FacturaSchema, db: Session = Depends(get_db)):
    actualizado = (
        db.query(Documento)
        .filter(Documento.id_de == factura.id_de)
        .update({"estado_actual": "Enviado/Esperando consulta"})
    )
    db.commit()

    if actualizado == 0:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
