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


class Operacion(Base):
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
    drucem = Column(String(20))
    ddvemi = Column(SmallInteger)
    itipcont = Column(SmallInteger)
    ctipreg = Column(SmallInteger)
    dnomemi = Column(String(255))
    ddiremi = Column(String(255))
    dnumcas = Column(String(10))
    cdepemi = Column(SmallInteger)
    ddesdepemi = Column(String(50))
    cciuemi = Column(SmallInteger)
    ddesciuemi = Column(String(50))
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
