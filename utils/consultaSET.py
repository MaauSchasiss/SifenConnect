from datetime import datetime
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Documento, Estado


def consultaSet(id_de: str, db: Session):
    # 1️⃣ Buscar el documento por id_de
    doc = db.query(Documento).filter(Documento.id_de == id_de).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # 2️⃣ Obtener el CDC
    cdc = doc.cdc_de
    print(f"Simulando envío de documento con CDC {cdc} a la SET...")

    # 3️⃣ Simular respuesta aleatoria de la SET
    estados_simulados = [
        ("0301", "Documento procesado correctamente (Aprobado)"),
        ("0302", "Documento rechazado por error en firma electrónica"),
        ("0303", "Documento pendiente de procesamiento")
    ]
    dCodRes, dMsgRes = random.choice(estados_simulados)

    # 4️⃣ Crear registro del nuevo estado
    nuevo_estado = Estado(
        de_id=doc.id,
        dcodres=dCodRes,
        dmsgres=dMsgRes,
        dfecproc=datetime.now()
    )

    db.add(nuevo_estado)
    db.commit()
    db.refresh(nuevo_estado)

    # 5️⃣ (Opcional) actualizar estado_actual del documento
    doc.estado_actual = dMsgRes
    db.commit()

    # 6️⃣ Devolver resultado simulado
    return {
        "cdc": cdc,
        "dCodRes": dCodRes,
        "dMsgRes": dMsgRes,
        "dFecProc": nuevo_estado.dfecproc.strftime("%Y-%m-%dT%H:%M:%S")
    }
    