# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

# ---------------------------
# Operacion
# ---------------------------
class OperacionSchema(BaseModel):
    itipemi: int = Field(..., ge=1, le=2)
    ddestipemi: str = Field(..., max_length=12)
    dcodseg: str = Field(..., max_length=9)
    dinfoemi: Optional[str] = Field(None, max_length=3000)
    dinfosc: Optional[str] = Field(None, max_length=3000)

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
    cacteco: str = Field(..., max_length=8)
    ddesacteco: str = Field(..., max_length=300)

class EmisorSchema(BaseModel):
    drucem: str = Field(..., max_length=8)
    ddvemi: int = Field(..., ge=0, le=9)
    itipcont: int = Field(..., ge=1, le=2)
    ctipreg: Optional[int] = None
    dnomemi: str = Field(..., max_length=255)
    ddiremi: str = Field(..., max_length=255)
    dnumcas: str = Field(..., max_length=6)
    cdepemi: Optional[int] = None
    ddesdepemi: Optional[str] = Field(None, max_length=16)
    cciuemi: Optional[int] = None
    ddesciuemi: Optional[str] = Field(None, max_length=30)
    dtelem: Optional[str] = Field(None, max_length=15)
    demail: Optional[str] = Field(None, max_length=80)
    actividades: Optional[List[EmisorActividadSchema]] = Field(default_factory=list)

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

# ---------------------------
# Documento raíz
# ---------------------------
class FacturaSchema(BaseModel):
    id_de: str = Field(..., max_length=44)
    dverfor: int = Field(..., ge=100, le=999)
    ddvid: int = Field(..., ge=0, le=9)
    dfecfirma: datetime
    dsisfact: int = Field(..., ge=1, le=2)

    operacion: OperacionSchema
    timbrado: TimbradoSchema
    emisor: EmisorSchema
    receptor: ReceptorSchema
    items: List[ItemSchema] = Field(default_factory=list)
    totales: TotalesSchema