# schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
import re
# ---------------------------
# Operacion
# ---------------------------
class OperacionSchema(BaseModel):
    itipemi: int = Field(..., ge=1, le=2)
    ddestipemi: str = Field(..., max_length=12)
    dcodseg: str = Field(..., max_length=9)
    dinfoemi: Optional[str] = Field(None, max_length=3000)
    dinfofisc: Optional[str] = Field(None, max_length=3000)

# ---------------------------
# Timbrado
# ---------------------------
class TimbradoSchema(BaseModel):
    itide: int = Field(..., ge=1, le=8)
    ddestide: str = Field(..., max_length=40)
    dnumtim: str = Field(..., max_length=8)
    dest: str = Field(..., max_length=3)
    dpunexp: str = Field(..., max_length=3)
    dnumdoc: str = Field(..., max_length=7)
    dserienum: Optional[str] = Field(None, max_length=2)
    dfeinit: date

# ---------------------------
# Emisor
# ---------------------------
class EmisorActividadSchema(BaseModel):
    cacteco: str = Field(..., min_length=1, max_length=20)
    ddesacteco: str = Field(..., min_length=1, max_length=255)

    class Config:
        from_attributes = True

class EmisorSchema(BaseModel):
    drucem: str = Field(..., min_length=3, max_length=8)  # D101: RUC (3-8 caracteres)
    ddvemi: int = Field(..., ge=0, le=9)  # D102: Dígito verificador
    itipcont: int = Field(..., ge=1, le=2)  # D103: Tipo de contribuyente (1=Persona Física, 2=Persona Jurídica)
    ctipreg: Optional[int] = Field(None, ge=1, le=99)  # D104: Tipo de régimen (1-2 dígitos) - OPCIONAL
    dnomemi: str = Field(..., min_length=4, max_length=255)  # D105: Nombre o razón social
    dnomfanemi: Optional[str] = Field(None, min_length=4, max_length=255)  # D106: Nombre de fantasía - OPCIONAL
    ddiremi: str = Field(..., min_length=1, max_length=255)  # D107: Dirección principal
    dnumcas: str = Field(..., min_length=1, max_length=6)  # D108: Número de casa
    dcompdir1: Optional[str] = Field(None, max_length=255)  # D109: Complemento dirección 1 - OPCIONAL
    dcompdir2: Optional[str] = Field(None, max_length=255)  # D110: Complemento dirección 2 - OPCIONAL
    cdepemi: int = Field(..., ge=1, le=99)  # D111: Código departamento
    ddesdepemi: str = Field(..., min_length=6, max_length=16)  # D112: Descripción departamento
    cdisemi: Optional[int] = Field(None, ge=1, le=9999)  # D113: Código distrito - OPCIONAL
    ddesdisemi: Optional[str] = Field(None, max_length=30)  # D114: Descripción distrito - OPCIONAL
    cciuremi: int = Field(..., ge=1, le=99999)  # D115: Código ciudad emisión
    ddesciuremi: str = Field(..., min_length=1, max_length=30)  # D116: Descripción ciudad emisión
    dtelem: str = Field(..., min_length=6, max_length=15)  # D117: Teléfono (6-15 caracteres)
    demail: str = Field(..., min_length=3, max_length=80)  # D118: Email (3-80 caracteres)
    ddensuc: Optional[str] = Field(None, max_length=30)  # D119: Denominación comercial sucursal - OPCIONAL
    
    actividades: Optional[List[EmisorActividadSchema]] = Field(default_factory=list)

    # Validadores
    @validator('dnumcas')
    def validate_dnumcas(cls, v):
        if not re.match(r'^[0-9]{1,6}$', v):
            raise ValueError('dnumcas debe contener solo números y tener entre 1-6 dígitos')
        return v

    @validator('drucem')
    def validate_drucem(cls, v):
        if not re.match(r'^[0-9]{3,8}$', v):
            raise ValueError('drucem debe contener solo números y tener entre 3-8 dígitos')
        return v

    @validator('demail')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('demail debe ser una dirección de correo válida')
        return v

    @validator('dtelem')
    def validate_telephone(cls, v):
        if not re.match(r'^[0-9+\-\s()]{6,15}$', v):
            raise ValueError('dtelem debe ser un número de teléfono válido')
        return v

    class Config:
        from_attributes = True
# ---------------------------
# Receptor
# ---------------------------
class ReceptorSchema(BaseModel):
    inatrec: int = Field(..., ge=1, le=2)
    itiope: int = Field(..., ge=1, le=4)
    cpaisrec: str = Field(..., max_length=3)
    ddespaisre: str = Field(..., max_length=30)
    iticontrec: Optional[int] = Field(None, ge=1, le=2)
    drucrec: Optional[str] = Field(None, max_length=8)
    ddvrec: Optional[int] = Field(None, ge=0, le=9)
    dnomrec: str = Field(..., max_length=255)
    ddirrec: Optional[str] = Field(None, max_length=255)
    dnumcasrec: Optional[str] = Field(None, max_length=6)
    cdeprec: Optional[int] = None
    ddesdeprec: Optional[str] = Field(None, max_length=16)
    cdisrec: Optional[int] = None
    ddesdisrec: Optional[str] = Field(None, max_length=30)
    cciurec: Optional[int] = None
    ddesciurec: Optional[str] = Field(None, max_length=30)
    dtelrec: Optional[str] = Field(None, max_length=15)
    dcodcliente: Optional[str] = Field(None, max_length=15)

# ---------------------------
# Item
# ---------------------------
class ItemValorRestaSchema(BaseModel):
    ddescitem: Decimal = Field(default=0, max_digits=15, decimal_places=8)
    dporcdesit: Optional[Decimal] = Field(None, max_digits=3, decimal_places=8)
    ddescgloitem: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)
    dtotopeitem: Decimal = Field(..., max_digits=15, decimal_places=8)

class ItemValorSchema(BaseModel):
    dpuniproser: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotbruopeitem: Decimal = Field(..., max_digits=15, decimal_places=8)
    valor_resta: ItemValorRestaSchema

class ItemIvaSchema(BaseModel):
    iafeciva: int = Field(..., ge=1, le=4)
    ddesafeciva: str = Field(..., max_length=15)
    dpropiva: Decimal = Field(..., ge=0, le=100)  # Corregido: porcentaje entre 0-100
    dtasaiva: Decimal = Field(..., ge=0, le=100)  
    dbasgraviva: Decimal = Field(..., max_digits=15, decimal_places=8)
    dliqivaitem: Decimal = Field(..., max_digits=15, decimal_places=8)

class ItemSchema(BaseModel):
    dcodint: str = Field(..., max_length=20)
    ddesproser: str = Field(..., max_length=120)
    cuni_med: str = Field(..., max_length=5)
    ddesunimed: str = Field(..., max_length=10)
    dcantproser: Decimal = Field(..., max_digits=10, decimal_places=4)
    dinfitem: Optional[str] = Field(None, max_length=500)
    valor_item: ItemValorSchema
    iva: Optional[ItemIvaSchema] = None

# ---------------------------
# Totales
# ---------------------------
class TotalesSchema(BaseModel):
    dsubexe: Decimal = Field(..., max_digits=15, decimal_places=8)
    dsubexo: Decimal = Field(..., max_digits=15, decimal_places=8)
    dsub5: Decimal = Field(..., max_digits=15, decimal_places=8)
    dsub10: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotope: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotdesc: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotdescglotem: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotantitem: Decimal = Field(..., max_digits=15, decimal_places=8)
    dtotant: Decimal = Field(..., max_digits=15, decimal_places=8)
    dporcdesctotal: Decimal = Field(..., max_digits=3, decimal_places=8)
    ddesctotal: Decimal = Field(..., max_digits=15, decimal_places=8)
    danticipo: Decimal = Field(..., max_digits=15, decimal_places=8)
    dredon: Decimal = Field(..., max_digits=15, decimal_places=4)
    dtotgralope: Decimal = Field(..., max_digits=15, decimal_places=8)
    diva5: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)
    diva10: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)
    dtotiva: Decimal = Field(..., max_digits=15, decimal_places=8)
    dbasegrav5: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)
    dbasegrav10: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)
    dtbasgraiva: Optional[Decimal] = Field(None, max_digits=15, decimal_places=8)


class OperacionComercialSchema(BaseModel):
    itiptra: Optional[int] = Field(None, ge=1, le=13)
    ddestiptra: Optional[str] = Field(None, min_length=5, max_length=36)
    itimp: int = Field(..., ge=1, le=5)
    ddestimp: str = Field(..., min_length=3, max_length=11)
    cmoneope: str = Field(..., min_length=3, max_length=3)
    ddesmoneope: str = Field(..., min_length=3, max_length=20)
    dcondticam: Optional[int] = Field(None, ge=1, le=2)
    dticam: Optional[float] = Field(None, ge=0)
    icondant: Optional[int] = Field(None, ge=1, le=2)
    ddescondant: Optional[str] = Field(None, min_length=15, max_length=17)

    class Config:
        from_attributes = True


# ---------------------------
# Documento raíz
# ---------------------------
class FacturaSchema(BaseModel):
    id_de: str = Field(..., max_length=44)

    operacion: OperacionSchema
    timbrado: TimbradoSchema
    emisor: EmisorSchema
    receptor: ReceptorSchema
    items: List[ItemSchema] = Field(default_factory=list)
    totales: TotalesSchema
    operacion_comercial : OperacionComercialSchema
    
class NotaCreditoDebitoSchema(BaseModel):
    imotemi: int = Field(..., ge=1, le=8)
    ddesmotemi: str = Field(..., min_length=6, max_length=30)
    
    class Config:
        from_attributes = True
        
class EventoSchema(BaseModel):
    id_evento: str = Field(..., min_length=1, max_length=10)
    dfecfirma: datetime
    dverfor: int = Field(..., ge=1)
    dtigde: int = Field(..., ge=1, le=13)
    
    # Campos para CANCELACIÓN (dtigde = 1)
    cdc_dte: Optional[str] = Field(None, min_length=44, max_length=44)
    mototEve: Optional[str] = Field(None, min_length=5, max_length=500)
    
    # Campos para INUTILIZACIÓN (dtigde = 2)
    dnumtim: Optional[str] = Field(None, min_length=8, max_length=8)
    dest: Optional[str] = Field(None, min_length=3, max_length=3)
    dpunexp: Optional[str] = Field(None, min_length=3, max_length=3)
    dnumin: Optional[str] = Field(None, min_length=7, max_length=7)
    dnumfin: Optional[str] = Field(None, min_length=7, max_length=7)
    itide: Optional[int] = Field(None, ge=1, le=8)
    
    class Config:
        from_attributes = True

# ---------------------------
class EstadoSchema(BaseModel):
    cod_estado: str = Field(..., min_length=1, max_length=10)
    des_estado: str = Field(..., min_length=1, max_length=100)
    mensaje_respuesta: Optional[str] = None
    nro_transaccion: Optional[str] = Field(None, min_length=1, max_length=20)
    origen: Optional[str] = Field('SET', min_length=1, max_length=20)

    class Config:
        from_attributes = True

class ConsultaLoteSchema(BaseModel):
    nro_lote: str = Field(..., min_length=1, max_length=15)
    cod_respuesta_lote: Optional[int] = None
    msg_respuesta_lote: Optional[str] = Field(None, min_length=1, max_length=255)

    class Config:
        from_attributes = True

class ConsultaDocumentoSchema(BaseModel):
    consulta_lote_id: int
    documento_id: int
    cdc: str = Field(..., min_length=44, max_length=44)

    class Config:
        from_attributes = True
