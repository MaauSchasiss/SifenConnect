from datetime import datetime
from fastapi import HTTPException
from models import (
    Documento, Timbrado as TimbradoModel, Emisor as EmisorModel,
    EmisorActividad as EmisorActividadModel, Item as ItemModel,
    Totales as TotalesModel, OperacionComercial as OperacionComercialModel,
    NotaCreditoDebito as NotaCreditoDebitoModel, Operacion as OperacionModel
)
from schemas import FacturaSchema
from utils.simularConsu import simular_consulta_set
from utils.generarFechaEmi import generar_fecha_emision
from utils.generarFechaFirm import generar_fecha_firma
from utils.generarCodSeg import generar_codigo_seguridad
from utils.calcularDV import calcular_dv_11a
from utils.armarCDC import armarCDC
from utils.EnvioSET import envioAlaSET
from utils.consultaSET import consultaSet

def crear_documento(factura: FacturaSchema, itide: int, ddestide: str, incluir_nota: bool,db):
        try:
            # 1️⃣ Fechas
            dfeemide = datetime.strptime(generar_fecha_emision(), "%Y-%m-%dT%H:%M:%S")
            dfecfirma = datetime.strptime(generar_fecha_firma(dfeemide), "%Y-%m-%dT%H:%M:%S")

            # 2️⃣ Documento base
            doc = Documento(
                id_de=factura.id_de,
                ddvid=calcular_dv_11a(factura.id_de),
                dsisfact=1,
                dfeemide=dfeemide,
                dfecfirma=dfecfirma,
                dverfor=factura.dverfor
            )
            db.add(doc)
            db.flush()

            # 3️⃣ Timbrado
            timbrado = TimbradoModel(
                de_id=doc.id,
                itide=itide,
                ddestide=ddestide,
                dnumtim=factura.timbrado.dnumtim,
                dest=factura.timbrado.dest,
                dpunexp=factura.timbrado.dpunexp,
                dnumdoc=factura.timbrado.dnumdoc,
                dserienum=factura.timbrado.dserienum,
                dfeinit=factura.timbrado.dfeinit
            )
            db.add(timbrado)

            # 4️⃣ Operación
            dcodseg = generar_codigo_seguridad()
            operacion = OperacionModel(
                de_id=doc.id,
                itipemi=factura.operacion.itipemi,
                ddestipemi=factura.operacion.ddestipemi,
                dcodseg=dcodseg,
                dinfoemi=factura.operacion.dinfoemi,
                dinfofisc=factura.operacion.dinfofisc
            )
            db.add(operacion)
            factura.operacion.dcodseg = dcodseg

            # 5️⃣ Operación comercial (si existe)
            if factura.operacion_comercial:
                db.add(OperacionComercialModel(
                    de_id=doc.id,
                    itiptra=factura.operacion_comercial.itiptra,
                    ddestiptra=factura.operacion_comercial.ddestiptra,
                    itimp=factura.operacion_comercial.itimp,
                    ddestimp=factura.operacion_comercial.ddestimp,
                    cmoneope=factura.operacion_comercial.cmoneope,
                    ddesmoneope=factura.operacion_comercial.ddesmoneope,
                    dcondticam=factura.operacion_comercial.dcondticam,
                    dticam=factura.operacion_comercial.dticam,
                    icondant=factura.operacion_comercial.icondant,
                    ddescondant=factura.operacion_comercial.ddescondant
                ))

            # 6️⃣ Emisor (con cálculo DV si falta)
            if getattr(factura.emisor, "ddvemi", None) is None:
                factura.emisor.ddvemi = calcular_dv_11a(factura.emisor.drucem)

            emisor = EmisorModel(
                de_id=doc.id,
                drucem=factura.emisor.drucem,
                ddvemi=factura.emisor.ddvemi,
                itipcont=factura.emisor.itipcont,
                ctipreg=factura.emisor.ctipreg,
                dnomemi=factura.emisor.dnomemi,
                ddiremi=factura.emisor.ddiremi,
                dnumcas=factura.emisor.dnumcas,
                cdepemi=factura.emisor.cdepemi,
                ddesdepemi=factura.emisor.ddesdepemi,
                cciuremi=factura.emisor.cciuremi,
                ddesciuremi=factura.emisor.ddesciuremi,
                dtelem=factura.emisor.dtelem,
                demail=factura.emisor.demail
            )
            db.add(emisor)
            db.flush()

            for act in getattr(factura.emisor, "actividades", []) or []:
                db.add(EmisorActividadModel(
                    emisor_id=emisor.id,
                    cacteco=act.cacteco,
                    ddesacteco=act.ddesacteco
                ))

            # 7️⃣ Items
            for item in factura.items or []:
                db.add(ItemModel(
                    de_id=doc.id,
                    dcodint=item.dcodint,
                    ddesproser=item.ddesproser,
                    cuni_med=item.cuni_med,
                    ddesunimed=item.ddesunimed,
                    dcantproser=item.dcantproser,
                    dpuniproser=item.valor_item.dpuniproser,
                    dtotbruopeitem=item.valor_item.dtotbruopeitem,
                    ddescitem=item.valor_item.valor_resta.ddescitem,
                    dtotopeitem=item.valor_item.valor_resta.dtotopeitem
                ))

            # 8️⃣ Nota crédito/débito si aplica
            if incluir_nota and factura.nota_credito_debito:
                db.add(NotaCreditoDebitoModel(
                    de_id=doc.id,
                    imotemi=factura.nota_credito_debito.imotemi,
                    ddesmotemi=factura.nota_credito_debito.ddesmotemi
                ))

            # 9️⃣ Totales
            db.add(TotalesModel(
                de_id=doc.id,
                dsubexe=factura.totales.dsubexe,
                dtotiva=factura.totales.dtotiva
            ))

            # 10️⃣ CDC
            factura.dfecfirma = dfecfirma
            factura.dfeemide = dfeemide
            cdc = armarCDC(factura=factura)
            doc.cdc_de = cdc
            db.add(doc)

            # 11️⃣ Envío SET (aca deberia de ir el response y guardar en el estado )
            envioAlaSET(factura=factura, db=db)
            if itide == 1:
                consultaSet(factura.id_de, db=db)

            db.commit()
            return {"msg": f"{ddestide} creada correctamente", "id_de": doc.id_de}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))