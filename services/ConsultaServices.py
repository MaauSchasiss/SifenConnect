from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Documento,Estado as EstadoModel 
from utils.simularConsu import simular_consulta_set


class ConsultaServices:
    def __init__(self,db:Session):
        self.db = db
        
    def consulta(self,cdc: str,):
        
        estado = (
            self.db.query(EstadoModel)
            .join(Documento, EstadoModel.de_id == Documento.id)
            .filter(Documento.cdc_de == cdc)
            .order_by(EstadoModel.dfecproc.desc())
            .first()
        )

        if estado:
            return {
                "cdc": cdc,
                "dFecProc": estado.dfecproc.strftime("%Y-%m-%dT%H:%M:%S"),
                "dCodRes": estado.dcodres,
                "dMsgRes": estado.dmsgres,
            }

        # 2️⃣ Verificar si el CDC existe en la base
        documento = self.db.query(Documento).filter(Documento.cdc_de == cdc).first()
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        # 3️⃣ Simular llamada a la SET
        respuesta_simulada = simular_consulta_set(cdc)

        # 4️⃣ Guardar el nuevo estado
        nuevo_estado = EstadoModel(
            de_id=documento.id,
            dcodres=respuesta_simulada["dCodRes"],
            dmsgres=respuesta_simulada["dMsgRes"],
            dfecproc=datetime.strptime(respuesta_simulada["dFecProc"], "%Y-%m-%dT%H:%M:%S"),
        )

        self.db.add(nuevo_estado)
        self.db.commit()

        return {
            "cdc": cdc,
            "dFecProc": respuesta_simulada["dFecProc"],
            "dCodRes": respuesta_simulada["dCodRes"],
            "dMsgRes": respuesta_simulada["dMsgRes"],
        }