from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session ,joinedload
from schemas import EventoSchema
from models import Documento, Evento as EventoModel 
from utils.inutilizacion import simulacionInutilizacion

class InutilizacionServices:
    def __init__(self,db=Session):
        self.db = db
    
    def inutilizacion(self,evento=EventoSchema):          
        try:
                
                documento = (
                    self.db.query(Documento)
                    .options(joinedload(Documento.timbrado))
                    .filter(Documento.cdc_de == evento.cdc_dte)
                    .first()
                )
                if not documento:
                    raise HTTPException(status_code=404, detail="Documento no encontrado")

                
                tim = getattr(documento, "timbrado", None)
                dnumtim_val = evento.dnumtim or (tim.dnumtim if tim else None)
                dest_val = evento.dest or (tim.dest if tim else None)
                dpunexp_val = evento.dpunexp or (tim.dpunexp if tim else None)
                itide_val = evento.itide or (tim.itide if tim else None)
                mototeve_val = getattr(evento, "mototeve", None)

                campos = {
                    "dnumtim": dnumtim_val,
                    "dest": dest_val,
                    "dpunexp": dpunexp_val,
                    "dnumin": evento.dnumin,
                    "dnumfin": evento.dnumfin,
                    "itide": itide_val,
                    "mototeve": mototeve_val
                }

                faltantes = [nombre for nombre, valor in campos.items() if valor in (None, "")]

                if faltantes:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Faltan campos requeridos para inutilización: {', '.join(faltantes)}"
                )

                
                nuevo_evento = EventoModel(
                    id_evento=evento.id_evento,
                    dfecfirma=documento.dfecfirma,
                    dverfor=documento.dverfor,
                    dtigde=2,
                    cdc_dte=evento.cdc_dte,
                    dnumtim=dnumtim_val,
                    dest=dest_val,
                    dpunexp=dpunexp_val,
                    dnumin=evento.dnumin,
                    dnumfin=evento.dnumfin,
                    itide=itide_val,
                    mototeve=mototeve_val,
                    de_id=documento.id
                )
                self.db.add(nuevo_evento)
                # func envio a la set  # logica para request/response a la set
                self.db.commit()
                self.db.refresh(nuevo_evento)
                simulacionInutilizacion(cdc_de=nuevo_evento.cdc_dte, db=self.db)

                return {
                    "msg": "Evento de inutilización registrado correctamente",
                    "cdc_dte": nuevo_evento.cdc_dte
                }

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
            
