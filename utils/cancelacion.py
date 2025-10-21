from fastapi import HTTPException
from sqlalchemy.orm import Session
from models  import Documento

def simulacionCancelacion(cdc_de:str , db = Session ):
    # 1️⃣ Buscar el documento por id_de
    doc = db.query(Documento).filter(Documento.cdc_de == cdc_de).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")


    
    print(f"Cancelacion del DE con CDC :{cdc_de} enviado...")

    doc.estado_actual = "cancelado"
    db.commit()

    return f'Cancelado de forma exitosa'
