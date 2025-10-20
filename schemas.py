from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
import re

# ---------------------------
# Operacion
# ---------------------------
class OperacionSchema(BaseModel):
    itipemi: int = Field(..., alias="TipoEmision", ge=1, le=2)
    ddestipemi: str = Field(..., alias="DescriTipoEmision", max_length=12)
    dcodseg: Optional[str] = Field(None, alias="CodigoSeguridad", max_length=9)
    dinfoemi: Optional[str] = Field(None, alias="InfoEmisor", max_length=3000)
    dinfofisc: Optional[str] = Field(None, alias="InfoFiscal", max_length=3000)

    class Config:
        populate_by_name = True

# ---------------------------
# Timbrado
# ---------------------------
class TimbradoSchema(BaseModel):
    itide: int = Field(..., alias="TipoDocumento", ge=1, le=8)
    ddestide: str = Field(..., alias="DescriTipoDocumento", max_length=40)
    dnumtim: str = Field(..., alias="NumeroTimbrado", max_length=8)
    dest: str = Field(..., alias="Establecimiento", max_length=3)
    dpunexp: str = Field(..., alias="PuntoExpedicion", max_length=3)
    dnumdoc: str = Field(..., alias="NumeroDocumento", max_length=7)
    dserienum: Optional[str] = Field(None, alias="SerieNumero", max_length=2)
    dfeinit: date = Field(..., alias="FechaInicioVigencia")

    class Config:
        populate_by_name = True

# ---------------------------
# Emisor
# ---------------------------
class EmisorActividadSchema(BaseModel):
    cacteco: str = Field(..., alias="CodigoActividad", min_length=1, max_length=20)
    ddesacteco: str = Field(..., alias="DescripcionActividad", min_length=1, max_length=255)

    class Config:
        from_attributes = True
        populate_by_name = True


class EmisorSchema(BaseModel):
    drucem: str = Field(..., alias="RucEmisor", min_length=3, max_length=8)
    ddvemi: Optional[int] = Field(None, alias="DVEmisor", ge=0, le=9)  
    itipcont: int = Field(..., alias="TipoContribuyente", ge=1, le=2)
    ctipreg: Optional[int] = Field(None, alias="TipoRegimen", ge=1, le=99)
    dnomemi: str = Field(..., alias="RazonSocial", min_length=4, max_length=255)
    dnomfanemi: Optional[str] = Field(None, alias="NombreFantasia", min_length=4, max_length=255)
    ddiremi: str = Field(..., alias="Direccion", min_length=1, max_length=255)
    dnumcas: str = Field(..., alias="NumeroCasa", min_length=1, max_length=6)
    dcompdir1: Optional[str] = Field(None, alias="ComplementoDir1", max_length=255)
    dcompdir2: Optional[str] = Field(None, alias="ComplementoDir2", max_length=255)
    cdepemi: int = Field(..., alias="CodigoDepartamento", ge=1, le=99)
    ddesdepemi: str = Field(..., alias="DescriDepartamento", min_length=6, max_length=16)
    cdisemi: Optional[int] = Field(None, alias="CodigoDistrito", ge=1, le=9999)
    ddesdisemi: Optional[str] = Field(None, alias="DescriDistrito", max_length=30)
    cciuremi: int = Field(..., alias="CodigoCiudadEmision", ge=1, le=99999)
    ddesciuremi: str = Field(..., alias="DescriCiudadEmision", min_length=1, max_length=30)
    dtelem: str = Field(..., alias="TelefonoEmisor", min_length=6, max_length=15)
    demail: str = Field(..., alias="EmailEmisor", min_length=3, max_length=80)
    ddensuc: Optional[str] = Field(None, alias="DenominacionSucursal", max_length=30)

    actividades: Optional[List[EmisorActividadSchema]] = Field(default_factory=list, alias="Actividades")

    # Validaciones
    @validator('dnumcas')
    def validar_numero_casa(cls, v):
        if not re.match(r'^[0-9]{1,6}$', v):
            raise ValueError('NumeroCasa debe contener solo números (1-6 dígitos)')
        return v

    @validator('drucem')
    def validar_ruc(cls, v):
        if not re.match(r'^[0-9]{3,8}$', v):
            raise ValueError('RUC debe contener solo números (3-8 dígitos)')
        return v

    @validator('demail')
    def validar_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v

    @validator('dtelem')
    def validar_telefono(cls, v):
        if not re.match(r'^[0-9+\-\s()]{6,15}$', v):
            raise ValueError('Teléfono inválido')
        return v

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Receptor
# ---------------------------
class ReceptorSchema(BaseModel):
    inatrec: int = Field(..., alias="NaturalezaReceptor", ge=1, le=2)
    itiope: int = Field(..., alias="TipoOperacion", ge=1, le=4)
    cpaisrec: str = Field(..., alias="CodigoPais", max_length=3)
    ddespaisre: str = Field(..., alias="DescripcionPais", max_length=30)
    iticontrec: Optional[int] = Field(None, alias="TipoContribuyente", ge=1, le=2)
    drucrec: Optional[str] = Field(None, alias="RucReceptor", max_length=8)
    ddvrec: Optional[int] = Field(None, alias="DVReceptor", ge=0, le=9)
    dnomrec: str = Field(..., alias="NombreReceptor", max_length=255)
    ddirrec: Optional[str] = Field(None, alias="DireccionReceptor", max_length=255)
    dnumcasrec: Optional[str] = Field(None, alias="NumeroCasaReceptor", max_length=6)
    cdeprec: Optional[int] = Field(None, alias="CodigoDepartamentoReceptor")
    ddesdeprec: Optional[str] = Field(None, alias="DescripcionDepartamentoReceptor", max_length=16)
    cdisrec: Optional[int] = Field(None, alias="CodigoDistritoReceptor")
    ddesdisrec: Optional[str] = Field(None, alias="DescripcionDistritoReceptor", max_length=30)
    cciurec: Optional[int] = Field(None, alias="CodigoCiudadReceptor")
    ddesciurec: Optional[str] = Field(None, alias="DescripcionCiudadReceptor", max_length=30)
    dtelrec: Optional[str] = Field(None, alias="TelefonoReceptor", max_length=15)
    dcodcliente: Optional[str] = Field(None, alias="CodigoCliente", max_length=15)

    class Config:
        populate_by_name = True

# ---------------------------
# Item
# ---------------------------
class ItemValorRestaSchema(BaseModel):
    ddescitem: Decimal = Field(default=0, alias="DescuentoItem", max_digits=15, decimal_places=8)
    dporcdesit: Optional[Decimal] = Field(None, alias="PorcentajeDescuentoItem", max_digits=11, decimal_places=8)
    ddescgloitem: Optional[Decimal] = Field(None, alias="DescuentoGlobalItem", max_digits=15, decimal_places=8)
    dtotopeitem: Decimal = Field(..., alias="TotalOperacionItem", max_digits=15, decimal_places=8)

    class Config:
        populate_by_name = True


class ItemValorSchema(BaseModel):
    dpuniproser: Decimal = Field(..., alias="PrecioUnitario", max_digits=15, decimal_places=8)
    dtotbruopeitem: Decimal = Field(..., alias="TotalBrutoOperacionItem", max_digits=15, decimal_places=8)
    valor_resta: ItemValorRestaSchema = Field(..., alias="ValorResta")

    class Config:
        populate_by_name = True


class ItemIvaSchema(BaseModel):
    iafeciva: int = Field(..., alias="AfectacionIVA", ge=1, le=4)
    ddesafeciva: str = Field(..., alias="DescriAfectacionIVA", max_length=15)
    dpropiva: Decimal = Field(..., alias="ProporcionIVA", ge=0, le=100)
    dtasaiva: Decimal = Field(..., alias="TasaIVA", ge=0, le=100)
    dbasgraviva: Decimal = Field(..., alias="BaseGravadaIVA", max_digits=15, decimal_places=8)
    dliqivaitem: Decimal = Field(..., alias="LiquidoIVAItem", max_digits=15, decimal_places=8)

    class Config:
        populate_by_name = True


class ItemSchema(BaseModel):
    dcodint: str = Field(..., alias="CodigoInterno", max_length=20)
    ddesproser: str = Field(..., alias="DescripcionProductoServicio", max_length=120)
    cuni_med: str = Field(..., alias="CodigoUnidadMedida", max_length=5)
    ddesunimed: str = Field(..., alias="DescripcionUnidadMedida", max_length=10)
    dcantproser: Decimal = Field(..., alias="CantidadProductoServicio", max_digits=10, decimal_places=4)
    dinfitem: Optional[str] = Field(None, alias="InformacionItem", max_length=500)
    valor_item: ItemValorSchema = Field(..., alias="ValorItem")
    iva: Optional[ItemIvaSchema] = Field(None, alias="IVA")

    class Config:
        populate_by_name = True

# ---------------------------
# Totales
# ---------------------------
class TotalesSchema(BaseModel):
    dsubexe: Decimal = Field(..., alias="SubExentas", max_digits=15, decimal_places=8)
    dsubexo: Decimal = Field(..., alias="SubExoneradas", max_digits=15, decimal_places=8)
    dsub5: Decimal = Field(..., alias="Sub5", max_digits=15, decimal_places=8)
    dsub10: Decimal = Field(..., alias="Sub10", max_digits=15, decimal_places=8)
    dtotope: Decimal = Field(..., alias="TotalOperacion", max_digits=15, decimal_places=8)
    dtotdesc: Decimal = Field(0, alias="TotalDescuento", max_digits=15, decimal_places=8)
    dtotdescglotem: Decimal = Field(0, alias="TotalDescuentoGlobalItem", max_digits=15, decimal_places=8)
    dtotantitem: Decimal = Field(0, alias="TotalAnticipoItem", max_digits=15, decimal_places=8)
    dtotant: Decimal = Field(0, alias="TotalAnticipo", max_digits=15, decimal_places=8)
    dporcdesctotal: Decimal = Field(0, alias="PorceDescTotal", max_digits=11, decimal_places=8)
    ddesctotal: Decimal = Field(0, alias="DescTotal", max_digits=15, decimal_places=8)
    danticipo: Decimal = Field(0, alias="Anticipo", max_digits=15, decimal_places=8)
    dredon: Decimal = Field(0, alias="Redondeo", max_digits=15, decimal_places=4)
    dtotgralope: Decimal = Field(..., alias="TotalGralOperacion", max_digits=15, decimal_places=8)
    diva5: Optional[Decimal] = Field(None, alias="IVA5", max_digits=15, decimal_places=8)
    diva10: Optional[Decimal] = Field(None, alias="IVA10", max_digits=15, decimal_places=8)
    dtotiva: Decimal = Field(..., alias="TotalIVA", max_digits=15, decimal_places=8)
    dbasegrav5: Optional[Decimal] = Field(None, alias="BaseGrav5", max_digits=15, decimal_places=8)
    dbasegrav10: Optional[Decimal] = Field(None, alias="BaseGrav10", max_digits=15, decimal_places=8)
    dtbasgraiva: Optional[Decimal] = Field(None, alias="TotalBaseGravIVA", max_digits=15, decimal_places=8)

    class Config:
        populate_by_name = True

# ---------------------------
# Operacion Comercial
# ---------------------------
class OperacionComercialSchema(BaseModel):
    itiptra: Optional[int] = Field(None, alias="TipoTransaccion", ge=1, le=13)
    ddestiptra: Optional[str] = Field(None, alias="DescriTipoTransaccion", min_length=5, max_length=36)
    itimp: int = Field(..., alias="TipoImpuesto", ge=1, le=5)
    ddestimp: str = Field(..., alias="DescriTipoImpuesto", min_length=3, max_length=11)
    cmoneope: str = Field(..., alias="MonedaOperacion", min_length=3, max_length=3)
    ddesmoneope: str = Field(..., alias="DescriMonedaOperacion", min_length=3, max_length=20)
    dcondticam: Optional[int] = Field(None, alias="CondiTipoCambio", ge=1, le=2)
    dticam: Optional[float] = Field(None, alias="TipoCambio", ge=0)
    icondant: Optional[int] = Field(None, alias="CondicionAnticipo", ge=1, le=2)
    ddescondant: Optional[str] = Field(None, alias="DescriCondicionAnticipo", min_length=15, max_length=17)

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Nota Crédito/Débito
# ---------------------------
class NotaCreditoDebitoSchema(BaseModel):
    imotemi: int = Field(..., alias="MotivoEmision", ge=1, le=8)
    ddesmotemi: str = Field(..., alias="DescriMotivoEmision", min_length=6, max_length=30)

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Evento
# ---------------------------
class EventoSchema(BaseModel):
    id_evento: str = Field(..., alias="IdEvento", min_length=1, max_length=10)
    cdc_dte: Optional[str] = Field(None, alias="CodigoDeControl", min_length=44, max_length=44)
    mototeve: Optional[str] = Field(None, alias="MotivoEvento", min_length=5, max_length=500)
    dnumtim: Optional[str] = Field(None, alias="NumeroTimbrado", min_length=8, max_length=8)
    dest: Optional[str] = Field(None, alias="Establecimiento", min_length=3, max_length=3)
    dpunexp: Optional[str] = Field(None, alias="PuntoExpedicion", min_length=3, max_length=3)
    dnumin: Optional[str] = Field(None, alias="NumeroInicio", min_length=7, max_length=7)
    dnumfin: Optional[str] = Field(None, alias="NumeroFin", min_length=7, max_length=7)
    itide: Optional[int] = Field(None, alias="TipoDocumento", ge=1, le=8)

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Estado
# ---------------------------
class EstadoSchema(BaseModel):
    dcodres: str = Field(..., alias="CodigoResultado", min_length=1, max_length=10)
    dmsgres: str = Field(..., alias="MensajeResultado", min_length=1, max_length=255)
    dfecproc: Optional[datetime] = Field(None, alias="FechaProcesamiento")

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Consultas
# ---------------------------
class ConsultaLoteSchema(BaseModel):
    nro_lote: str = Field(..., alias="NumeroLote", min_length=1, max_length=15)
    cod_respuesta_lote: Optional[int] = Field(None, alias="CodigoRespuestaLote")
    msg_respuesta_lote: Optional[str] = Field(None, alias="MensajeRespuestaLote", min_length=1, max_length=255)

    class Config:
        from_attributes = True
        populate_by_name = True


class ConsultaDocumentoSchema(BaseModel):
    consulta_lote_id: int = Field(..., alias="IdConsultaLote")
    documento_id: int = Field(..., alias="IdDocumento")
    cdc: str = Field(..., alias="CodigoControl", min_length=44, max_length=44)

    class Config:
        from_attributes = True
        populate_by_name = True

# ---------------------------
# Documento raíz
# ---------------------------
class FacturaSchema(BaseModel):
    id_de: str = Field(..., alias="IdDE", max_length=44)
    dfeemide: Optional[datetime] = Field(None, alias="FechaEmision")
    dfecfirma: Optional[datetime] = Field(None, alias="FechaFirma")
    dverfor: int = Field(..., alias="VersionFormato")

    operacion: OperacionSchema = Field(..., alias="Operacion")
    timbrado: TimbradoSchema = Field(..., alias="Timbrado")
    emisor: EmisorSchema = Field(..., alias="Emisor")
    receptor: ReceptorSchema = Field(..., alias="Receptor")
    items: List[ItemSchema] = Field(default_factory=list, alias="Items")
    totales: TotalesSchema = Field(..., alias="Totales")
    operacion_comercial: OperacionComercialSchema = Field(..., alias="OperacionComercial")
    nota_credito_debito: Optional[NotaCreditoDebitoSchema] = Field(None, alias="NotaCreditoDebito")

    class Config:
        from_attributes = True
        populate_by_name = True
