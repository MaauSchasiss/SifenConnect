from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Datos de conexión (ajustá a tu entorno)
load_dotenv()

ENV = os.getenv("ENV", "Desarrollo")

if ENV.lower() == "produccion" :
    DATABASE_URL = os.getenv("DATABASE_URL")
else :
    DB_USER = "postgres"
    DB_PASSWORD = "7606"
    DB_HOST = "localhost"
    DB_NAME = "Sifen_API"
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()