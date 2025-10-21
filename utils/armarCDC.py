from typing import Optional
from models import Documento ,Emisor as EmisorModel ,Timbrado as TimbradoModel , Operacion as OperacionModel
from schemas import FacturaSchema
from sqlalchemy.orm import Session
from utils.calcularDV import calcular_dv_11a

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