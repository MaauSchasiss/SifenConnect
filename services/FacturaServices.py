from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel, NotaCreditoDebito as NotaCreditoDebitoModel,Evento as EventoModel,Operacion as OperacionModel,Estado as EstadoModel
from schemas import FacturaSchema , EventoSchema 
from utils.crearDocumento import crear_documento




class FacturaService:
    def __init__(self,db:Session):
        self.db = db
     
    def postFacturaElectronica(self,factura:FacturaSchema):
        "Factura Electronica "
    
        return crear_documento(
            factura=factura,
            itide=1,
            ddestide = "Factura Electrónica",
            incluir_nota = False,
            db = self.db
        )
        
    def postNotaCredito(self,factura:FacturaSchema):
        #nota credito 
        return crear_documento(
            factura=factura,
            itide=5,
            ddestide = "Nota de Crédito",
            incluir_nota = False,
            db = self.db
        )