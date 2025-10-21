from fastapi import HTTPException
from sqlalchemy.orm import Session 
from schemas import EventoSchema
from models import Documento, Evento as EventoModel 
from utils.cancelacion import simulacionCancelacion

 
class CancelacionServices:
    def __init__(self,db=Session):
        self.db = db
     
    def cancelacion(self,evento:EventoSchema):    

        try:
            documento = self.db.query(Documento).filter(Documento.cdc_de == evento.cdc_dte).first()
            if not documento:
                raise HTTPException(status_code=404, detail="Documento no encontrado")

            nuevo_evento = EventoModel(
                id_evento=evento.id_evento,
                dfecfirma=documento.dfecfirma,
                dverfor=documento.dverfor,
                dtigde=1, #Cancelacion
                cdc_dte=evento.cdc_dte,
                mototeve=evento.mototeve,
                de_id=documento.id
            )

            self.db.add(nuevo_evento)
            # Si envío externo falla, no confirmar
            # defs.envioEventoASeten(nuevo_evento, db) 
            
            self.db.commit()
            simulacionCancelacion(cdc_de=evento.cdc_dte,db=self.db)
            return {"msg": "Evento de cancelación registrado correctamente", "id_evento": evento.id_evento}

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))