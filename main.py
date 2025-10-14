from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Documento, Timbrado as TimbradoModel, Emisor as EmisorModel, EmisorActividad as EmisorActividadModel, Item as ItemModel, Totales as TotalesModel
from schemas import FacturaSchema

app = FastAPI()

@app.post("/Api/sifen/FE")
def crearFE(factura: FacturaSchema, db: Session = Depends(get_db)):
    
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
        itide=factura.timbrado.itide,
        ddestide=factura.timbrado.ddestide,
        dnumtim=factura.timbrado.dnumtim,
        dest=factura.timbrado.dest,
        dpunexp=factura.timbrado.dpunexp,
        dnumdoc=factura.timbrado.dnumdoc,
        dserienum=factura.timbrado.dserienum,
        dfeinit=factura.timbrado.dfeinit
    )
    db.add(timbrado)

    # Emisor
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
        cciuemi=factura.emisor.cciuemi,
        ddesciuemi=factura.emisor.ddesciuemi,
        dtelem=factura.emisor.dtelem,
        demail=factura.emisor.demail,
    )
    db.add(emisor)
    db.flush()  # para obtener emisor.id

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

    # Confirmar todo
    db.commit()

    return {"msg": "Factura electrónica creada correctamente", "id_de": doc.id_de}
