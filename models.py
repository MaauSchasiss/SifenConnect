from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Documento(Base):
    __tablename__ = "de_documento"
    id = Column(Integer, primary_key=True, index=True)
    id_de = Column(String(100), unique=True, nullable=False)
    dverfor = Column(Integer)
    ddvid = Column(Integer)
    dfecfirma = Column(TIMESTAMP)
    dsisfact = Column(SmallInteger)

    operacion = relationship("Operacion", back_populates="documento", uselist=False)
    timbrado = relationship("Timbrado", back_populates="documento", uselist=False)
    emisor = relationship("Emisor", back_populates="documento", uselist=False)
    receptor = relationship("Receptor", back_populates="documento", uselist=False)
    items = relationship("Item", back_populates="documento")
    totales = relationship("Totales", back_populates="documento", uselist=False)
    operacion_comercial = relationship("OperacionComercial", back_populates="documento", uselist=False)


class OperaciondeDE(Base):
    __tablename__ = "de_operacion"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    itipemi = Column(SmallInteger)
    ddestipemi = Column(String(50))
    dcodseg = Column(String(20))
    dinfoemi = Column(SmallInteger)
    dinfosc = Column(String(255))

    documento = relationship("Documento", back_populates="operacion")


class Timbrado(Base):
    __tablename__ = "de_timbrado"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    itide = Column(SmallInteger)
    ddestide = Column(String(50))
    dnumtim = Column(String(20))
    dest = Column(String(5))
    dpunexp = Column(String(5))
    dnumdoc = Column(String(20))
    dserienum = Column(String(10))
    dfeinit = Column(Date)

    documento = relationship("Documento", back_populates="timbrado")

class Emisor(Base):
    __tablename__ = "de_emisor"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    
    # Campos según especificación D100-D129
    drucem = Column(String(13))  # D101: RUC (3-13 caracteres)
    ddvemi = Column(SmallInteger)  # D102: Dígito verificador
    itipcont = Column(SmallInteger)  # D103: Tipo contribuyente (1,2)
    ctipreg = Column(SmallInteger)  # D104: Tipo régimen (1-2 dígitos)
    dnomemi = Column(String(255))  # D105: Nombre/Razón social
    dnomfanemi = Column(String(255))  # D106: Nombre fantasía (opcional)
    ddiremi = Column(String(255))  # D107: Dirección principal
    dnumcas = Column(String(6))  # D108: Número casa (1-6 caracteres)
    dcompdir1 = Column(String(255))  # D109: Complemento dirección 1 (opcional)
    dcompdir2 = Column(String(255))  # D110: Complemento dirección 2 (opcional)
    cdepemi = Column(SmallInteger)  # D111: Código departamento
    ddesdepemi = Column(String(16))  # D112: Descripción departamento (6-16 chars)
    cdisemi = Column(SmallInteger)  # D113: Código distrito (opcional)
    ddesdisemi = Column(String(30))  # D114: Descripción distrito (opcional)
    
    # Campos adicionales (si los necesitas)
    dtelem = Column(String(50))
    demail = Column(String(100))

    actividades = relationship("EmisorActividad", back_populates="emisor")
    documento = relationship("Documento", back_populates="emisor")

class EmisorActividad(Base):
    __tablename__ = "de_emisor_actividad"
    id = Column(Integer, primary_key=True)
    emis_id = Column(Integer, ForeignKey("de_emisor.id", ondelete="CASCADE"))
    cacteco = Column(String(20))
    ddesacteco = Column(String(255))

    emisor = relationship("Emisor", back_populates="actividades")


class Receptor(Base):
    __tablename__ = "de_receptor"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    inatrec = Column(SmallInteger)
    itiope = Column(SmallInteger)
    cpaisrec = Column(String(10))
    ddespaisre = Column(String(50))
    iticontrec = Column(SmallInteger)
    drucrec = Column(String(20))
    ddvrec = Column(SmallInteger)
    dnomrec = Column(String(255))
    ddirrec = Column(String(255))
    dnumcasrec = Column(String(10))
    cdeprec = Column(SmallInteger)
    ddesdeprec = Column(String(50))
    cdisrec = Column(SmallInteger)
    ddesdisrec = Column(String(50))
    cciurec = Column(SmallInteger)
    ddesciurec = Column(String(50))
    dtelrec = Column(String(50))
    dcodcliente = Column(String(50))

    documento = relationship("Documento", back_populates="receptor")


class Item(Base):
    __tablename__ = "de_item"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    dcodint = Column(String(50))
    ddesproser = Column(String(255))
    cuni_med = Column(String(10))
    ddesunimed = Column(String(20))
    dcantproser = Column(Numeric(15, 2))
    dinfitem = Column(String(100))
    dpuniproser = Column(Numeric(15, 2))
    dtotbruopeitem = Column(Numeric(15, 2))
    ddescitem = Column(Numeric(15, 2))
    dporcdesit = Column(Numeric(6, 2))
    ddescgloitem = Column(Numeric(15, 2))
    dtotopeitem = Column(Numeric(15, 2))
    iafeciva = Column(SmallInteger)
    ddesafeciva = Column(String(50))
    dpropiva = Column(Numeric(6, 2))
    dtasaiva = Column(Numeric(6, 2))
    dbasgraviva = Column(Numeric(15, 2))
    dliqivaitem = Column(Numeric(15, 2))

    documento = relationship("Documento", back_populates="items")


class Totales(Base):
    __tablename__ = "de_totales"
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    dsubexe = Column(Numeric(15,2))
    dsubexo = Column(Numeric(15,2))
    dsub5 = Column(Numeric(15,2))
    dsub10 = Column(Numeric(15,2))
    dtotope = Column(Numeric(15,2))
    dtotdesc = Column(Numeric(15,2))
    dtotdescglotem = Column(Numeric(15,2))
    dtotantitem = Column(Numeric(15,2))
    dtotant = Column(Numeric(15,2))
    dporcdesctotal = Column(Numeric(6,2))
    ddesctotal = Column(Numeric(15,2))
    danticipo = Column(Numeric(15,2))
    dredon = Column(Numeric(15,2))
    dtotgralope = Column(Numeric(15,2))
    diva5 = Column(Numeric(15,2))
    diva10 = Column(Numeric(15,2))
    dtotiva = Column(Numeric(15,2))
    dbasegrav5 = Column(Numeric(15,2))
    dbasegrav10 = Column(Numeric(15,2))
    dtbasgraiva = Column(Numeric(15,2))

    documento = relationship("Documento", back_populates="totales")

class OperacionComercial(Base):
    __tablename__ = "de_operacion_comercial"
    
    id = Column(Integer, primary_key=True)
    de_id = Column(Integer, ForeignKey("de_documento.id", ondelete="CASCADE"))
    itiptra = Column(SmallInteger)
    ddestiptra = Column(String(36))
    itimp = Column(SmallInteger, nullable=False)
    ddestimp = Column(String(11), nullable=False)
    cmoneope = Column(String(3), nullable=False)
    ddesmoneope = Column(String(20), nullable=False)
    dcondticam = Column(SmallInteger)
    dticam = Column(Numeric(9, 4))
    icondant = Column(SmallInteger)
    ddescondant = Column(String(17))
    
    documento = relationship("Documento", back_populates="operacion_comercial")