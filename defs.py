import secrets
import hashlib
from typing import Optional
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel, NotaCreditoDebito as NotaCreditoDebitoModel,Evento as EventoModel,Operacion as OperacionModel,Estado as EstadoModel
from schemas import FacturaSchema , EventoSchema
from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException


def calcular_dv_11a(numero: str, basemax: int = 11) -> int:
    """
    Calcula el dígito verificador (DV) usando el algoritmo módulo 11.
    Admite entrada alfanumérica (por ejemplo, RUC o cédula con letra final).
    """

    # Paso 1: Reemplazar letras por su código ASCII
    numero_al = ""
    for c in numero.upper():
        if c.isdigit():
            numero_al += c
        else:
            numero_al += str(ord(c))  # ord obtiene el valor ASCII

    # Paso 2: Calcular el DV
    k = 2
    total = 0

    for c in reversed(numero_al):
        if k > basemax:
            k = 2
        total += int(c) * k
        k += 1

    resto = total % 11
    if resto > 1:
        digito = 11 - resto
    else:
        digito = 0

    return digito




def generar_codigo_seguridad() -> str:
    """
    Genera un código de seguridad (dCodSeg) válido para SIFEN.
    - Número positivo de 9 dígitos
    - Aleatorio, no secuencial
    - No relacionado con datos del DE
    """
    # genera un número aleatorio entre 1 y 999999999
    codigo = secrets.randbelow(999_999_999) + 1
    
    # convierte a string y completa con ceros a la izquierda si hace falta
    return f"{codigo:09d}"






def armarCDC(db: Session = None, id_de: str = None, factura: Optional[FacturaSchema] = None) -> str:
    """
    Genera el CDC concatenando campos en orden según la documentación.
    Todos los campos se rellenan con ceros a la izquierda si corresponde.
    """
    if factura is None:
        if db is None or id_de is None:
            raise ValueError("Se requiere factura en memoria o db+id_de para generar CDC")
        doc = db.query(Documento).filter(Documento.id_de == id_de).first()
        if not doc:
            raise ValueError("Documento no encontrado en BD")
        emisor = db.query(EmisorModel).filter(EmisorModel.de_id == doc.id).first()
        timbrado = db.query(TimbradoModel).filter(TimbradoModel.de_id == doc.id).first()
        class _F: pass
        factura = _F()
        factura.id_de = doc.id_de
        factura.dfecfirma = doc.dfecfirma
        factura.emisor = emisor
        factura.timbrado = timbrado
        factura.operacion = db.query(OperacionModel).filter(OperacionModel.de_id == doc.id).first()

    # Validar campos obligatorios
    faltantes = []
    if not getattr(factura, "emisor", None):
        faltantes.append("Emisor")
    else:
        for campo in ["drucem", "ddvemi", "itipcont"]:
            if getattr(factura.emisor, campo, None) is None:
                faltantes.append(f"Emisor.{campo}")

    if not getattr(factura, "timbrado", None):
        faltantes.append("Timbrado")
    else:
        for campo in ["itide", "dest", "dpunexp", "dnumdoc"]:
            if getattr(factura.timbrado, campo, None) is None:
                faltantes.append(f"Timbrado.{campo}")

    if not getattr(factura, "operacion", None):
        faltantes.append("Operacion")
    else:
        for campo in ["itipemi", "dcodseg"]:
            if getattr(factura.operacion, campo, None) is None:
                faltantes.append(f"Operacion.{campo}")

    if not getattr(factura, "dfecfirma", None):
        faltantes.append("Documento.dfecfirma")

    if faltantes:
        raise ValueError(f"Faltan los siguientes datos para generar el CDC: {', '.join(faltantes)}")

    # Construir CDC según orden de la imagen
    cdc = (
        str(factura.timbrado.itide).zfill(2) +
        str(factura.emisor.drucem).zfill(8) +
        str(factura.emisor.ddvemi) +
        str(factura.timbrado.dest).zfill(3) +
        str(factura.timbrado.dpunexp).zfill(3) +
        str(factura.timbrado.dnumdoc).zfill(7) +
        str(factura.emisor.itipcont) +
        factura.dfecfirma.strftime("%Y%m%d") +
        str(factura.operacion.itipemi) +
        str(factura.operacion.dcodseg).zfill(9)
    )

    dv_cdc = calcular_dv_11a(cdc)
    return f"{cdc}{dv_cdc}"

    
from datetime import datetime, timedelta

def generar_fecha_firma(fecha_transmision: datetime = None) -> str:
    """
    Genera la fecha de firma digital del DE en formato AAAA-MM-DDThh:mm:ss.
    La fecha de firma debe ser anterior a la fecha de transmisión.
    """
    if fecha_transmision is None:
        fecha_transmision = datetime.now()
    
    # Para seguridad, se puede poner la firma 1 segundo antes de la transmisión
    fecha_firma = fecha_transmision - timedelta(seconds=1)
    
    return fecha_firma.strftime("%Y-%m-%dT%H:%M:%S")

from datetime import datetime, timedelta

def generar_fecha_emision(fecha_transmision: datetime = None, ajuste_horas: int = 0) -> str:
    """
    Genera la fecha de emisión del DE en formato AAAA-MM-DDThh:mm:ss
    con los límites de 720 horas atrás y 120 horas adelante respecto a la fecha de transmisión.
    
    :param fecha_transmision: fecha/hora actual de transmisión (por defecto ahora)
    :param ajuste_horas: ajuste opcional en horas (puede ser negativo o positivo)
    :return: string de fecha en formato KuDE
    """
    if fecha_transmision is None:
        fecha_transmision = datetime.now()
    
    # Límite máximo y mínimo
    max_fecha = fecha_transmision + timedelta(hours=120)   # +5 días
    min_fecha = fecha_transmision - timedelta(hours=720)   # -30 días
    
    # Fecha ajustada
    fecha_ajustada = fecha_transmision + timedelta(hours=ajuste_horas)
    
    # Aplicar límites
    if fecha_ajustada > max_fecha:
        fecha_ajustada = max_fecha
    elif fecha_ajustada < min_fecha:
        fecha_ajustada = min_fecha
    
    # Formato AAAA-MM-DDThh:mm:ss
    return fecha_ajustada.strftime("%Y-%m-%dT%H:%M:%S")


def envioAlaSET(factura: FacturaSchema, db: Session = Depends(get_db)):
    
    doc = Documento(
        estado_actual = "Enviado/Esperando consulta"
    )
    db.add(doc)
    db.flush()

