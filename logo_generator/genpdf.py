from fpdf import FPDF
from PIL import Image

# === DATI SNEAKERS ===

dunk_high_pure_platinum = {
    "nome": "Summit White Pure Platinum - Nike Dunk High",
    "taglia": "US 10.5 / EU 44.5",
    "valore": "103 EUR",
    "link": "https://stockx.com/nike-dunk-high-summit-white-pure-platinum"
}

dunk_high_ambush = {
    "nome": "AMBUSH Deep Royal - Nike Dunk High",
    "taglia": "US 8.5 / EU 42",
    "valore": "220 EUR",
    "link": "https://stockx.com/nike-dunk-high-ambush-deep-royal"
}

air_jordan_one_travis = {
    "nome": "Fragment x Travis Scott - Jordan 1 Retro Low OG SP",
    "taglia": "US 12.5 / EU 47.5",
    "valore": "1.500 EUR",
    "link": "https://stockx.com/air-jordan-1-retro-low-og-sp-fragment-x-travis-scott"
}

dunk_high_magnus = {
    "nome": "Ishod Wair x Magnus Walker - Nike SB Dunk High Pro",
    "taglia": "US 10.5 / EU 44.5",
    "valore": "310 EUR",
    "link": "https://stockx.com/nike-sb-dunk-high-pro-ishod-wair-x-magnus-walker"
}

ciabatte_stussy = {
    "nome": "Stussy Cream - Nike Benassi",
    "taglia": "US 7 / EU 40",
    "valore": "50 EUR",
    "link": "https://stockx.com/nike-benassi-stussy-cream"
}

jordan_four_sb = {
    "nome": "White Navy Blue - Jordan 4 SB",
    "taglia": "US 10 / EU 44",
    "valore": "250 EUR",
    "link": "https://stockx.com/it-it/air-jordan-4-retro-sb-navy"
}

travis_saturn = {
    "nome": "Travis Scott Cactus Jack Saturn Gold - Nike Air Max 1",
    "taglia": "US 4.5 / EU 36.5",
    "valore": "200 EUR",
    "link": "https://stockx.com/nike-air-max-1-travis-scott-cactus-jack-saturn-gold"
}

jordan_four_zen = {
    "nome": "Zen Master - Jordan 4 Retro",
    "taglia": "US 12 / EU 46",
    "valore": "250 EUR",
    "link": "https://stockx.com/air-jordan-4-retro-zen-master"
}

# === LISTA SNEAKERS ===

sneakers = [
    dunk_high_ambush,
    jordan_four_sb,
    jordan_four_zen,
    travis_saturn,
    air_jordan_one_travis,
    ciabatte_stussy,
    dunk_high_magnus,
]

# === LOGO ===
logo_path = "logo.png"  # Assicurati che il file sia presente

# === FUNZIONE PER ESTRARRE VALORE NUMERICO ===
def estrai_valore_numero(valore_str):
    try:
        valore_str = valore_str.lower().replace("eur", "").replace(".", "").replace(",", ".").strip()
        return float(valore_str)
    except:
        return 0.0

# === PDF SETUP ===
def generate_pdf(output_path="MarmoStock_SneakerList.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Calcola proporzioni e inserisce logo
    image = Image.open(logo_path)
    logo_width = 50  # in mm
    logo_height = int((logo_width / image.width) * image.height)
    pdf.image(logo_path, x=80, y=10, w=logo_width, h=logo_height)
    pdf.ln(logo_height + 10)

    # Aggiungi sneakers
    valore_totale = 0.0

    for s in sneakers:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, s["nome"])
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 10, f"Taglia Uomo: {s['taglia']}", ln=True)
        pdf.cell(0, 10, f"Valore attuale: {s['valore']}", ln=True)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", style='U', size=11)
        pdf.cell(0, 10, "Link StockX", ln=True, link=s["link"])
        pdf.ln(5)

        valore_totale += estrai_valore_numero(s["valore"])

    # === Valore Totale ===
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", style='B', size=13)
    pdf.cell(0, 10, f"Valore totale della collezione: {round(valore_totale)} EUR", ln=True)

    # Salva PDF
    pdf.output(output_path)
    print(f"PDF generato: {output_path}")

# === ESECUZIONE ===
if __name__ == "__main__":
    generate_pdf()
