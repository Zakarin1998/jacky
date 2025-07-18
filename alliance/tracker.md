# 📊 Finance Tracker CLI

Una semplice ma potente applicazione a riga di comando per la gestione delle finanze personali, scritta in Python e strutturata in modo modulare e orientata agli oggetti (OOP).

Segue una breve spiegazione dei casi d’uso ed esempi pratici.

---

## 📁 Struttura del progetto

```plaintext
finance_tracker/
│
├── main.py                         # Interfaccia CLI con Typer
│
├── models/                         # Definizione entità: User, Income, Expense
│   ├── __init__.py
│   ├── user.py
│   ├── income.py
│   └── expense.py
│
├── storage/                        # Persistenza dati su file JSON
│   ├── __init__.py
│   └── json_store.py
│
├── services/                       # Logica di business e gestione dati
│   ├── __init__.py
│   └── tracker.py
│
└── README.md                       # Documentazione del progetto
```

---

## 🚀 Funzionalità principali

* 👤 Gestione profilo utente (età, ISEE, regione, etc.)
* ➕ Aggiunta di **entrate** e **spese**
* 🧾 Gestione delle **spese deducibili**
* 📋 Elenco filtrato di dati salvati (entrate, uscite, deduzioni)
* 📈 Riepilogo finanziario con saldo netto

---

## 🧱 Requisiti

* Python 3.8+
* [Typer](https://typer.tiangolo.com) (`pip install "typer[all]"`)

---

## 📦 Installazione

```bash
git clone https://github.com/tuo-utente/finance-tracker-cli.git
cd finance-tracker-cli
pip install "typer[all]"
```

---

## 📌 Utilizzo

### 🎯 Gestione Profilo

Imposta o aggiorna i dati del profilo utente tramite opzioni:

```bash
python main.py profile --eta 27 --isee 25716 --regione Piemonte
```

Visualizza il profilo corrente:

```bash
python main.py profile
```

---

### ➕ Aggiungi un’entrata

```bash
python main.py add-income 1200 "Stipendio mensile"
```

---

### ➖ Aggiungi una spesa

```bash
python main.py add-expense 400 affitto --deductible --notes "Gennaio"
```

---

### 📋 Elenca dati

Lista di entrate:

```bash
python main.py list-items incomes
```

Lista di uscite:

```bash
python main.py list-items expenses
```

Lista di spese deducibili:

```bash
python main.py list-items deductibles
```

---

### 📈 Riepilogo finanziario

```bash
python main.py summary
```

## 🔒 Persistenza dati

I dati sono salvati in un file JSON nella home directory dell’utente:

```bash
~/.finance_tracker.json
```

---

## 🛠️ Roadmap futura

* [ ] Supporto database SQL (SQLite, PostgreSQL)
* [ ] Esportazione dati in CSV/PDF
* [ ] Gestione multi-utente
* [ ] Interfaccia web e mobile

---

## 📜 Licenza

MIT License
