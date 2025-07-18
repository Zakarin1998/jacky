# 📊 Finance Tracker CLI

Una semplice ma potente applicazione a riga di comando per la gestione delle finanze personali, scritta in Python e strutturata in modo modulare e OOP.

Segue una breve spiegazione dei casi d'uso ed esempi

---

## 📁 Struttura finale aggiornata

```plaintext
finance_tracker/
│
├── main.py                      # CLI principale con Typer
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── income.py
│   └── expense.py
│
├── storage/
│   ├── __init__.py
│   └── json_store.py
│
├── services/
│   ├── __init__.py
│   └── tracker.py
│
└── README.md                    # Documentazione del progetto
```

---

## 🚀 Funzionalità principali

- 👤 Gestione profilo utente (età, ISEE, etc.)
- ➕ Aggiunta di **entrate** e **spese**
- 🧾 Riconoscimento automatico delle **spese deducibili**
- 📋 Elenco filtrato di dati salvati
- 📈 Riepilogo finanziario con saldo netto

---

## 🧱 Requisiti

- Python 3.8+
- [Typer](https://typer.tiangolo.com) (`pip install typer[all]`)

---

## 📦 Installazione

```bash
git clone https://github.com/tuo-utente/finance-tracker-cli.git
cd finance-tracker-cli
pip install typer[all]
````

---

## 📌 Utilizzo

### 🎯 Profilo

```bash
python main.py profile --set eta=27 isee=25716 regione=Piemonte
```

### ➕ Aggiungi un'entrata

```bash
python main.py add-income 1200 "Stipendio mensile"
```

### ➖ Aggiungi una spesa

```bash
python main.py add-expense 400 affitto --deductible --notes "gennaio"
```

### 📃 Elenca dati

```bash
python main.py list-items incomes
python main.py list-items expenses
python main.py list-items deductibles
```

### 📈 Riepilogo

```bash
python main.py summary
```

---

## 📁 Struttura del progetto

```plaintext
finance_tracker/
├── main.py                  # Interfaccia CLI con Typer
├── models/                  # Definizione entità: User, Income, Expense
├── storage/                 # Persistenza dei dati su file JSON
├── services/                # Logica di business
└── README.md
```

---

## 🔒 Dati

I dati sono salvati in un file JSON all’interno della home dell’utente:

```bash
~/.finance_tracker.json
```

---

## 🛠️ Roadmap futura

* [ ] Supporto a SQLite o PostgreSQL
* [ ] Esportazione in CSV/PDF
* [ ] Supporto a più utenti
* [ ] Interfaccia web o mobile

---

## 📜 Licenza

MIT License
