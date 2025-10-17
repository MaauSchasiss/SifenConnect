from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel, NotaCreditoDebito as NotaCreditoDebitoModel,Evento as EventoModel,Operacion as OperacionModel
from schemas import FacturaSchema , EventoSchema
import defs

app = FastAPI()

@app.post("/Api/sifen/FE")
def postFE(factura: FacturaSchema, db: Session = Depends(get_db)):
    
    dfeemide = datetime.strptime(defs.generar_fecha_emision(), "%Y-%m-%dT%H:%M:%S")
    dfecfirma =datetime.strptime(defs.generar_fecha_firma(dfeemide), "%Y-%m-%dT%H:%M:%S")

    
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
    
    operacion = OperacionModel(
        de_id = doc.id,
        itipemi = factura.operacion.itipemi,
        ddestipemi = factura.operacion.ddestipemi,
        dcodseg = defs.generar_codigo_seguridad,
        dinfoemi = factura.operacion.dinfoemi,
        dinfofisc = factura.operacion.dinfosc
    )
    db.add(operacion)

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
        cciuremi=factura.emisor.cciuemi,  # Asegúrate que este campo existe en tu data
        ddesciuremi=factura.emisor.ddesciuemi,  # Asegúrate que este campo existe en tu data
        dtelem=factura.emisor.dtelem,
        demail=factura.emisor.demail,
        ddensuc=getattr(factura.emisor, 'ddensuc', None),
        actividades=[]  # O procesa las actividades si las tienes
    )
    db.add(emisor)
    db.flush()

    # Actividades del emisor
    for act in factura.emisor.actividades:
        actividad = EmisorActividadModel(
            emis_id=emisor.id,
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

    # Totales
    totales = TotalesModel(
        de_id=doc.id,
        dsubexe=factura.totales.dsubexe,
        dtotiva=factura.totales.dtotiva
    )
    db.add(totales)

    db.commit()
    
    defs.armarCDC(db,doc.id_de)

    return {"msg": "Factura electrónica creada correctamente", "id_de": doc.id_de}


@app.post("/Api/sifen/NC")
def postNC(factura: FacturaSchema, db: Session = Depends(get_db)):
    

    
    dfeemide = datetime.strptime(defs.generar_fecha_emision(), "%Y-%m-%dT%H:%M:%S")
    dfecfirma =datetime.strptime(defs.generar_fecha_firma(dfeemide), "%Y-%m-%dT%H:%M:%S")

    
    doc = Documento(
        id_de=factura.id_de,
        ddvid=defs.calcular_dv_11a(factura.id_de),
        dsisfact=1,
        dfeemide = dfeemide,
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
        dcodseg = defs.generar_codigo_seguridad,
        dinfoemi = factura.operacion.dinfoemi,
        dinfofisc = factura.operacion.dinfosc
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
        de_id=doc.id,
        drucem=factura.emisor.drucem,
        ddvemi=defs.calcular_dv_11a(factura.emisor.drucem),
        itipcont=factura.emisor.itipcont,
        ctipreg=factura.emisor.ctipreg,
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
        dtelem=factura.emisor.dtelem,
        demail=factura.emisor.demail,
    )
    db.add(emisor)
    db.flush()

    # Actividades del emisor
    for act in factura.emisor.actividades:
        actividad = EmisorActividadModel(
            emis_id=emisor.id,
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

    db.commit()

    return {"msg": "Nota de crédito creada correctamente", "id_de": doc.id_de}


@app.post("/Api/sifen/evento/cancelacion")
def postCancelacion(evento: EventoSchema, db: Session = Depends(get_db)):
    # Validar que sea tipo cancelación
    if evento.dtigde != 1:
        raise HTTPException(status_code=400, detail="Tipo de evento debe ser 1 (Cancelación)")
    
    # Buscar el documento por CDC
    documento = db.query(Documento).filter(Documento.id_de == evento.cdc_dte).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Crear evento de cancelación
    nuevo_evento = EventoModel(
        id_evento=evento.id_evento,
        dfecfirma=evento.dfecfirma,
        dverfor=evento.dverfor,
        dtigde=evento.dtigde,
        cdc_dte=evento.cdc_dte,
        mototEve=evento.mototEve,
        de_id=documento.id
    )
    
    db.add(nuevo_evento)
    db.commit()
    #logica de envio a la SET del evento cancelacion y guardado de response
    
    
    return {"msg": "Evento de cancelación registrado correctamente", "id_evento": evento.id_evento}


@app.post("/Api/sifen/evento/inutilizacion")
def postInutilizacion(evento: EventoSchema, db: Session = Depends(get_db)):
    # Validar que sea tipo inutilización
    if evento.dtigde != 2:
        raise HTTPException(status_code=400, detail="Tipo de evento debe ser 2 (Inutilización)")
    
    # Validar campos requeridos para inutilización
    if not all([evento.dnumtim, evento.dest, evento.dpunexp, evento.dnumin, evento.dnumfin, evento.itide]):
        raise HTTPException(status_code=400, detail="Faltan campos requeridos para inutilización")
    
    # Crear evento de inutilización
    nuevo_evento = EventoModel(
        id_evento=evento.id_evento,
        dfecfirma=evento.dfecfirma,
        dverfor=evento.dverfor,
        dtigde=evento.dtigde,
        # Campos de inutilización
        dnumtim=evento.dnumtim,
        dest=evento.dest,
        dpunexp=evento.dpunexp,
        dnumin=evento.dnumin,
        dnumfin=evento.dnumfin,
        itide=evento.itide,
        mototEve=evento.mototEve
    )
    
    db.add(nuevo_evento)
    db.commit()
    
    #logica de envio a la SET del evento inutilizacion y guardado de response
    
    return {"msg": "Evento de inutilización registrado correctamente", "id_evento": evento.id_evento}

