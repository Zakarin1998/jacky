# JCD Dashboard Backend

## Deploy to Railway
1. Fork or clone this repo.
2. In Railway, create a new project from GitHub repo.
3. Add environment variables in Railway settings (copiare da `.env.template`).
4. Railway rileverà `Procfile` e userà `runtime.txt` e `requirements.txt`.

## Local Setup
1. Copy `.env.template` → `.env` e popola.
2. `pip install -r requirements.txt`
3. `python app.py`

## API Endpoints
- `GET /api/price-status`
- `POST /api/generate-qr` (JSON `{data, logo_path}`)

---

## Completamento delle implementazioni
Questa roadmap di massima consente di ultimare la messa in produzione del backend su Railway, al fine di prepararsi allo sviluppo di un frontend professionale e performante.

1. **Finire `monitor/price_monitor.py`**

   * Inserire gli ABI completi di V1 Pair e V3 Pool.
   * Verificare che `get_v1_price()` e `get_v3_price()` ritornino valori corretti (scrivere piccoli script di sanity check).
   * Aggiungere gestione dei casi di errore più dettagliata (es. RPC timeout, pair non esistente).

2. **Completare `qr/qr_generator.py`**

   * Copiare esattamente il codice che già funzionava in `app.py` nel modulo `qr_generator.py`.
   * Aggiungere alcuni test locali per generare QR con logo e verificare output.

3. **Implementare test automatizzati**

   * **Unit tests** per le funzioni di prezzo (mocking di web3) e per il generatore QR (controllo dimensioni, presenza file).
   * **Integration test** per l’endpoint `/api/price-status`: simula una chiamata REST e controlla la risposta JSON.
   * **Integration test** per `/api/generate-qr`: invia un payload di prova e verifica che arrivi un PNG.

4. **CI / Linting / Formattazione**

   * Aggiungi un workflow GitHub Actions (o GitLab CI) che:

     * Esegue `flake8`/`pylint`
     * Esegue i test (`pytest`)
     * Controlla che non ci siano segreti nel repo
   * Imposta `black` in pre‑commit per formattazione coerente.

---

## 2. Preparazione al deploy su Railway

1. **Verifica locale del deploy**

   * Crea un piccolo `docker-compose` (opzionale) per simulare ambiente di produzione con Gunicorn.
   * Avvia `Procfile` localmente con `heroku local` o `railway up` per test.

2. **Configurazione Railway**

   * Importa il repo GitHub in Railway e crea un nuovo servizio “Web”.
   * Incolla le variabili d’ambiente (RPC\_URL, V1\_PAIR\_ADDRESS, …) copiate da `.env.template`.
   * Abilita “Deploy on push” per automaticità.

3. **Monitoring e logging**

   * Configura su Railway un add‑on di log (o invio su Papertrail): raccogli i file di log di `jcd_monitor.log` o stampali a stdout.
   * Aggiungi alert via e‑mail/Slack se la tua azione diventa `ALERT` (puoi inviare un webhook da dentro `log_prices()`).

---

## 3. Documentazione e accesso

1. **README.md**

   * Completa le sezioni “Local Setup” e “Deploy to Railway” con comandi esatti.
   * Fornisci esempi di payload per testare gli endpoint via `curl` o `httpie`.

2. **Swagger / OpenAPI**

   * Aggiungi un piccolo spec OpenAPI (puoi farlo inline con Flask‑RESTX o FastAPI in futuro)
   * Renderizza `/docs` per chi voglia provare l’API.

---

## 4. Passi successivi verso il frontend

1. **Definizione requisiti UI**

   * Bozza rapide di wireframe: pagina monitoraggio live e pagina QR generator.
2. **Scegliere tecnologia frontend**

   * React/Vue/Svelte, integrazione con Tailwind e librerie di chart (Recharts, Chart.js).
3. **Implementare pagine di prova**

   * `/status` → grafico tempo‑reale del prezzo e spread.
   * `/qr` → form per inserire testo/logo e mostrare il QR generato.

---

Con questo piano dovresti avere una guida passo‑passo per passare da prototipo a servizio “production‑ready” su Railway, con test, documentazione e monitoraggio. Fammi sapere se vuoi dettagli più precisi su un punto in particolare!
