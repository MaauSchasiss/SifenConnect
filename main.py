from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel, OperacionComercial as OperacionComercialModel
from schemas import FacturaSchema

app = FastAPI()

@app.post("/Api/sifen/FE")
def postFE(factura: FacturaSchema, db: Session = Depends(get_db)):
    
    doc = Documento(
        id_de=factura.id_de,
        ddvid=factura.ddvid,
        dfecfirma=factura.dfecfirma,
        dsisfact=factura.dsisfact
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
        ddestide=factura.emisor.ddestide,
        itipcont=factura.emisor.itipcont,
        ctipreg=factura.emisor.ctipreg,
        dnomemi=factura.emisor.dnomemi,
        ddiremi=factura.emisor.ddiremi,
        dnumcas=factura.emisor.dnumcas,
        cdepemi=factura.emisor.cdepemi,
        ddesdepemi=factura.emisor.ddesdepemi,
        cciuemi=factura.emisor.cciuemi,
        ddesciuemi=factura.emisor.ddesciuemi,
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

    # Totales
    totales = TotalesModel(
        de_id=doc.id,
        dsubexe=factura.totales.dsubexe,
        dtotiva=factura.totales.dtotiva
    )
    db.add(totales)

    db.commit()

    return {"msg": "Factura electrónica creada correctamente", "id_de": doc.id_de}

@app.post("/Api/sifen/NC")
def postNC(factura: FacturaSchema, db: Session = Depends(get_db)):
    
    doc = Documento(
        id_de=factura.id_de,
        ddvid=factura.ddvid,
        dfecfirma=factura.dfecfirma,
        dsisfact=factura.dsisfact
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
        ddvemi=factura.emisor.ddvemi,
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

    # Totales
    totales = TotalesModel(
        de_id=doc.id,
        dsubexe=factura.totales.dsubexe,
        dtotiva=factura.totales.dtotiva
    )
    db.add(totales)

    db.commit()

    return {"msg": "Nota de crédito creada correctamente", "id_de": doc.id_de}