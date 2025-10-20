from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel, NotaCreditoDebito as NotaCreditoDebitoModel,Evento as EventoModel,Operacion as OperacionModel,Estado as EstadoModel
from schemas import FacturaSchema , EventoSchema
import defs

app = FastAPI()

@app.post("/Api/sifen/FE")
def postFE(factura: FacturaSchema, db: Session = Depends(get_db)):
    try:
        dfeemide = datetime.strptime(defs.generar_fecha_emision(), "%Y-%m-%dT%H:%M:%S")
        dfecfirma = datetime.strptime(defs.generar_fecha_firma(dfeemide), "%Y-%m-%dT%H:%M:%S")

        doc = Documento(
            id_de=factura.id_de,
            ddvid=defs.calcular_dv_11a(factura.id_de),
            dsisfact=1,
            dfeemide=dfeemide,
            dfecfirma=dfecfirma,
            dverfor=factura.dverfor
        )
        db.add(doc)
        db.flush()

        # Timbrado
        timbrado = TimbradoModel(
            de_id=doc.id,
            itide=1,
            ddestide="Factura Electrónica",
            dnumtim=factura.timbrado.dnumtim,
            dest=factura.timbrado.dest,
            dpunexp=factura.timbrado.dpunexp,
            dnumdoc=factura.timbrado.dnumdoc,
            dserienum=factura.timbrado.dserienum,
            dfeinit=factura.timbrado.dfeinit
        )
        db.add(timbrado)

        # generar dcodseg y crear operacion (mantener en memoria)
        dcodseg = defs.generar_codigo_seguridad()
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

        # Operación Comercial
        operacion_comercial = OperacionComercialModel(
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
        )
        db.add(operacion_comercial)

        # Emisor
        emisor = EmisorModel(
            drucem=factura.emisor.drucem,
            ddvemi=defs.calcular_dv_11a(factura.emisor.drucem),
            itipcont=factura.emisor.itipcont,
            ctipreg=getattr(factura.emisor, 'ctipreg', None),
            dnomemi=factura.emisor.dnomemi,
            dnomfanemi=getattr(factura.emisor, 'dnomfanemi', None),
            ddiremi=factura.emisor.ddiremi,
            dnumcas=factura.emisor.dnumcas,
            dcompdir1=getattr(factura.emisor, 'dcompdir1', None),
            dcompdir2=getattr(factura.emisor, 'dcompdir2', None),
            cdepemi=factura.emisor.cdepemi,
            ddesdepemi=factura.emisor.ddesdepemi,
            cdisemi=getattr(factura.emisor, 'cdisemi', None),
            ddesdisemi=getattr(factura.emisor, 'ddesdisemi', None),
            cciuremi=factura.emisor.cciuremi,
            ddesciuremi=factura.emisor.ddesciuremi,
            dtelem=factura.emisor.dtelem,
            demail=factura.emisor.demail,
            ddensuc=getattr(factura.emisor, 'ddensuc', None)
        )
        db.add(emisor)
        db.flush()

        # Actividades del emisor
        for act in getattr(factura.emisor, "actividades", []) or []:
            actividad = EmisorActividadModel(
                emisor_id=emisor.id,
                cacteco=act.cacteco,
                ddesacteco=act.ddesacteco
            )
            db.add(actividad)

        # Items
        for item in factura.items or []:
            db_item = ItemModel(
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
            )
            db.add(db_item)

        # Totales
        totales = TotalesModel(
            de_id=doc.id,
            dsubexe=factura.totales.dsubexe,
            dtotiva=factura.totales.dtotiva
        )
        db.add(totales)

        # enriquecer factura en memoria
        factura.dfecfirma = dfecfirma
        factura.dfeemide = dfeemide

        # generar CDC usando datos en memoria
        cdc = defs.armarCDC(factura=factura)
        doc.cdc_de = cdc
        db.add(doc)

        # envío a la SET (si falla, no se confirma la transacción)
        defs.envioAlaSET(factura=factura, db=db)
        defs.consultaSet(factura.id_de, db=db)

        # todo validado -> confirmar una sola vez
        db.commit()
        return {"msg": "Factura electrónica creada correctamente", "id_de": doc.id_de}

    except Exception as e:
        db.rollback()
        # evita exponer trace; devuelve mensaje manejable
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/Api/sifen/NC")
def postNC(factura: FacturaSchema, db: Session = Depends(get_db)):
    try:
        dfeemide = datetime.strptime(defs.generar_fecha_emision(), "%Y-%m-%dT%H:%M:%S")
        dfecfirma = datetime.strptime(defs.generar_fecha_firma(dfeemide), "%Y-%m-%dT%H:%M:%S")

        doc = Documento(
            id_de=factura.id_de,
            ddvid=defs.calcular_dv_11a(factura.id_de),
            dsisfact=1,
            dfeemide=dfeemide,
            dfecfirma=dfecfirma
        )
        db.add(doc)
        db.flush()

        # Timbrado
        timbrado = TimbradoModel(
            de_id=doc.id,
            itide=2,
            ddestide="Nota de crédito electrónica",
            dnumtim=factura.timbrado.dnumtim,
            dest=factura.timbrado.dest,
            dpunexp=factura.timbrado.dpunexp,
            dnumdoc=factura.timbrado.dnumdoc,
            dserienum=factura.timbrado.dserienum,
            dfeinit=factura.timbrado.dfeinit
        )
        db.add(timbrado)
        
        operacion = OperacionModel(
            de_id = doc.id,
            itipemi = factura.operacion.itipemi,
            ddestipemi = factura.operacion.ddestipemi,
            dcodseg = defs.generar_codigo_seguridad(),
            dinfoemi = factura.operacion.dinfoemi,
            dinfofisc = factura.operacion.dinfofisc
        )

        # Operación Comercial
        operacion_comercial = OperacionComercialModel(
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
        )
        db.add(operacion_comercial)

        # Emisor
        emisor = EmisorModel(
            drucem=factura.emisor.drucem,
            ddvemi=defs.calcular_dv_11a(factura.emisor.drucem),
            itipcont=factura.emisor.itipcont,
            ctipreg=getattr(factura.emisor, 'ctipreg', None),
            dnomemi=factura.emisor.dnomemi,
            dnomfanemi=getattr(factura.emisor, 'dnomfanemi', None),
            ddiremi=factura.emisor.ddiremi,
            dnumcas=factura.emisor.dnumcas,
            dcompdir1=getattr(factura.emisor, 'dcompdir1', None),
            dcompdir2=getattr(factura.emisor, 'dcompdir2', None),
            cdepemi=factura.emisor.cdepemi,
            ddesdepemi=factura.emisor.ddesdepemi,
            cdisemi=getattr(factura.emisor, 'cdisemi', None),
            ddesdisemi=getattr(factura.emisor, 'ddesdisemi', None),
            cciuremi=factura.emisor.cciuremi,
            ddesciuremi=factura.emisor.ddesciuremi,
            dtelem=factura.emisor.dtelem,
            demail=factura.emisor.demail,
            ddensuc=getattr(factura.emisor, 'ddensuc', None)
        )
        db.add(emisor)
        db.flush()
        # Actividades del emisor
        for act in factura.emisor.actividades:
            actividad = EmisorActividadModel(
                emisor_id=emisor.id,
                cacteco=act.cacteco,
                ddesacteco=act.ddesacteco
            )
            db.add(actividad)

        # Items
        for item in factura.items:
            db_item = ItemModel(
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
            )
            db.add(db_item)
      
        # nota_cd
        
        nota_cd = NotaCreditoDebitoModel(
            de_id=doc.id,
            imotemi=factura.nota_credito_debito.imotemi,
            ddesmotemi=factura.nota_credito_debito.ddesmotemi
        )
        db.add(nota_cd)

        # Totales
        totales = TotalesModel(
            de_id=doc.id,
            dsubexe=factura.totales.dsubexe,
            dtotiva=factura.totales.dtotiva
        )
        db.add(totales)

        # enriquecer factura en memoria
        factura.dfecfirma = dfecfirma
        factura.dfeemide = dfeemide
        
        # generar CDC usando los datos en memoria 
        cdc = defs.armarCDC(factura=factura)
        doc.cdc_de = cdc
        db.add(doc)

        # envío a la SET (si falla, no se confirma la transacción)
        defs.envioAlaSET(factura=factura, db=db)

        db.commit()
        return {"msg": "Nota de crédito/débito creada correctamente", "id_de": doc.id_de}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/Api/sifen/evento/cancelacion")
def postCancelacion(evento: EventoSchema, db: Session = Depends(get_db)):
    try:
        documento = db.query(Documento).filter(Documento.cdc_de == evento.cdc_dte).first()
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

        db.add(nuevo_evento)
        # Si envío externo falla, no confirmar
        # defs.envioEventoASeten(nuevo_evento, db) 
        
        db.commit()
        defs.cancelacion(cdc_de=evento.cdc_dte,db=db)
        return {"msg": "Evento de cancelación registrado correctamente", "id_evento": evento.id_evento}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.post("/Api/sifen/evento/inutilizacion")
def postInutilizacion(evento: EventoSchema, db: Session = Depends(get_db)):
    try:
        # buscar el documento asociado por CDC
        documento = (
            db.query(Documento)
            .options(joinedload(Documento.timbrado))
            .filter(Documento.cdc_de == evento.cdc_dte)
            .first()
        )
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        # Resolver campos: preferir valores del evento, si faltan usar los del timbrado del documento
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

        # crear el registro del evento usando los valores resueltos
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
        db.add(nuevo_evento)
        # defs.envioEventoASeten(nuevo_evento, db)  # lo dejarías para más adelante
        db.commit()
        db.refresh(nuevo_evento)
        defs.inutilizacion(cdc_de=nuevo_evento.cdc_dte, db=db)

        return {
            "msg": "Evento de inutilización registrado correctamente",
            "cdc_dte": nuevo_evento.cdc_dte
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    



@app.get("/Api/sifen/consulta/{cdc}")
def consultar_estado_cdc(cdc: str, db: Session = Depends(get_db)):
    """
    Consulta el estado de un CDC:
    1. Busca si ya existe un estado guardado.
    2. Si no existe, verifica si el CDC pertenece a un documento.
    3. Si existe el documento pero no el estado, simula una consulta a la SET.
    """

    estado = (
        db.query(EstadoModel)
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
    documento = db.query(Documento).filter(Documento.cdc_de == cdc).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # 3️⃣ Simular llamada a la SET
    respuesta_simulada = defs.simular_consulta_set(cdc)

    # 4️⃣ Guardar el nuevo estado
    nuevo_estado = EstadoModel(
        de_id=documento.id,
        dcodres=respuesta_simulada["dCodRes"],
        dmsgres=respuesta_simulada["dMsgRes"],
        dfecproc=datetime.strptime(respuesta_simulada["dFecProc"], "%Y-%m-%dT%H:%M:%S"),
    )

    db.add(nuevo_estado)
    db.commit()

    return {
        "cdc": cdc,
        "dFecProc": respuesta_simulada["dFecProc"],
        "dCodRes": respuesta_simulada["dCodRes"],
        "dMsgRes": respuesta_simulada["dMsgRes"],
    }
