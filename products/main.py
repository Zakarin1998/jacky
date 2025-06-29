from database import SessionLocal
from models import Product

db = SessionLocal()

prodotti = db.query(Product).all()
for p in prodotti:
    print(f"{p.nome} – {p.categoria.value} – €{p.valore_attuale_eur}")

db.close()