from models import Product, Categoria
from database import SessionLocal, engine, Base

# Crea le tabelle
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    prodotti = [
        Product(
            nome="Fragment x Travis Scott – Jordan 1 Retro Low OG SP",
            categoria=Categoria.scarpe,
            taglia_us="12.5",
            taglia_eu="47.5",
            valore_attuale_eur=1500,
        ),
        Product(
            nome="Supreme – Tee bianca con Emilio Pucci",
            categoria=Categoria.maglietta,
            taglia_us="S",
            valore_attuale_eur=200,
        ),
        Product(
            nome="Supreme – Scatola rossa con bombolette",
            categoria=Categoria.accessori,
            valore_attuale_eur=80,
        ),
    ]
    db.add_all(prodotti)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()