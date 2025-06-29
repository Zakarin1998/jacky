from sqlalchemy import Column, String, Float, Integer, Enum
from database import Base
import enum


class Categoria(enum.Enum):
    scarpe = "scarpe"
    maglietta = "maglietta"
    accessori = "accessori"
    ciabatte = "ciabatte"


class Product(Base):
    __tablename__ = "prodotti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(Enum(Categoria), nullable=False)
    valore_attuale_eur = Column(Float, nullable=False)
    taglia_us = Column(String, nullable=True)
    taglia_eu = Column(String, nullable=True)
    link_immagine_fronte = Column(String, nullable=True)
    link_immagine_retro = Column(String, nullable=True)
    link_stockx = Column(String, nullable=True)
