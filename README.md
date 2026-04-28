# ✅ Todo List — Esercizio TDD da 1 ora

**Corso:** Software Testing Avanzato — EPICODE
**Durata:** 60 minuti
**Consegna:** repository GitHub con pipeline CI verde

---

## 📖 Contesto

Devi costruire una **To Do List** full stack applicando TDD (Test Driven Development).
Il dominio è volutamente semplice: l'obiettivo non è la complessità del software, ma padroneggiare il processo — scrivere i test prima del codice, a ogni livello dello stack.

---

## ⏱ Scaletta consigliata

| Fase | Tempo | Cosa fai |
|------|-------|----------|
| Setup | 5 min | Clone, `pip install`, `npm install` |
| Unit test Python | 15 min | Scrivi i test per `TodoList` in `tests/unit/` |
| Implementazione Python | 10 min | Implementa `models.py` e `app.py` fino al verde |
| Integration test | 10 min | Scrivi i test Flask in `tests/integration/` |
| Unit test JS + E2E | 10 min | Scrivi i test Vitest + 2 scenari Playwright |
| CI pipeline | 10 min | Scrivi `.github/workflows/ci.yml` |

---

## 🎯 Specifiche funzionali

### Entità: TodoItem

Ogni attività ha:
- un **id** univoco (generato automaticamente)
- un **titolo** (stringa non vuota, max 100 caratteri)
- uno stato **done** (booleano, parte a `false`)

### Comportamenti della lista

| Operazione | Descrizione |
|-----------|-------------|
| `add(title)` | Aggiunge un'attività. Lancia `ValueError` se il titolo è vuoto o solo spazi |
| `complete(id)` | Marca l'attività come completata. Lancia `KeyError` se l'id non esiste |
| `delete(id)` | Rimuove l'attività. Lancia `KeyError` se l'id non esiste |
| `clear_completed()` | Rimuove tutte le attività completate, ritorna quante ne ha rimosse |
| `all()` | Ritorna tutte le attività |
| `count` | Numero totale di attività |
| `pending_count` | Numero di attività non ancora completate |

### API REST (Flask)

| Metodo | Path | Descrizione |
|--------|------|-------------|
| `GET` | `/health` | `{"status": "ok"}` |
| `GET` | `/todos` | Lista tutti i todo con `count` e `pending` |
| `POST` | `/todos` | Crea un todo. Body: `{"title": "..."}` |
| `PATCH` | `/todos/<id>/complete` | Marca come completato |
| `DELETE` | `/todos/<id>` | Elimina un todo |
| `DELETE` | `/todos/completed` | Elimina tutti i completati |

**Comportamenti attesi:**
- `POST /todos` con titolo vuoto o assente → `400 Bad Request`
- `PATCH` o `DELETE` su id inesistente → `404 Not Found`
- `POST /todos` con titolo valido → `201 Created`

### Frontend JavaScript

Una pagina web (`index.html`) che permette di:
1. Aggiungere un todo (input + bottone, anche con tasto Invio)
2. Completare un todo cliccando un pulsante su ogni riga
3. Eliminare un todo
4. Filtrare per: Tutti / Attivi / Completati
5. Eliminare tutti i completati
6. Vedere il conteggio delle attività rimanenti

La logica di presentazione (formattazione etichette, filtraggio, validazione, ordinamento) deve stare in un modulo puro `todo-logic.js` senza dipendenze da DOM o fetch.

---

## ✅ Requisiti tecnici

### 1. Unit test Python (`pytest`) — scrivi PRIMA del codice
Testa ogni metodo di `TodoList` e `TodoItem` in isolamento.
Usa il ciclo **🔴 RED → 🟢 GREEN → 🔵 REFACTOR**.

### 2. Integration test Python (`pytest` + Flask test client)
Testa ogni endpoint HTTP. Usa una fixture che pulisce lo stato prima di ogni test.
Includi almeno un test multi-step (es. crea → completa → verifica contatori).

### 3. Unit test JavaScript (`Vitest`)
Testa `todo-logic.js` in isolamento (nessun fetch, nessun DOM).

### 4. E2E test (`Playwright`)
Testa il flusso completo nel browser. Usa `data-testid` per i selettori.
Scrivi almeno questi scenari:
- Aggiungere un todo e vederlo nella lista
- Completare un todo e vedere l'aggiornamento del contatore
- Filtrare per "Attivi"

### 5. Code quality
- Python: `flake8 todo/` senza errori, `black --check todo/` verde
- JavaScript: `npm run lint` senza errori
- Coverage Python ≥ 80%

### 6. Pipeline CI (`ci.yml`)
- Job `backend`: lint → unit → integration → coverage
- Job `frontend`: lint → vitest → coverage
- Job `e2e`: parte **solo se** backend e frontend sono verdi
- Report Playwright caricato come artifact anche in caso di fallimento

---

## 📐 Struttura attesa

```
todo-tdd/
├── backend/
│   ├── todo/
│   │   ├── models.py       ← TodoItem, TodoList
│   │   └── app.py          ← Flask API
│   ├── tests/
│   │   ├── unit/           ← test_models.py
│   │   └── integration/    ← test_api.py
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── todo-logic.js   ← logica pura testabile
│   │   ├── todo-client.js  ← wrapper fetch
│   │   └── index.html
│   ├── tests/
│   │   └── todo-logic.test.js
│   ├── vitest.config.js
│   └── package.json
├── e2e/
│   └── todo.spec.js
├── playwright.config.js
└── .github/workflows/ci.yml
```

---


---

## 🐳 Esecuzione con Docker

Se preferisci non installare Python e Node localmente, puoi usare Docker.

### Prerequisiti
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installato e in esecuzione

### Avvio rapido

```bash
# Costruisci le immagini e avvia i container
docker compose up --build

# Apri il browser su http://localhost:3000
```

### Come funziona

```
Browser → http://localhost:3000
              │
              ▼
        nginx (frontend)
              │
              ├── /         → serve index.html, JS
              │
              └── /api/*    → proxy verso backend:5000/*
                                    │
                                    ▼
                            Flask (backend)
                            rete interna Docker
```

nginx fa da **reverse proxy**: il browser parla solo con nginx su porta 3000.
Le chiamate API vengono girate al backend sulla rete interna Docker,
eliminando completamente il problema CORS (stessa origine per il browser).

### Comandi utili

```bash
# Avvia in background
docker compose up --build -d

# Segui i log in tempo reale
docker compose logs -f

# Ferma i container
docker compose down

# Ricostruisci dopo modifiche al codice
docker compose up --build
```

### Test con Docker in esecuzione

Puoi continuare a eseguire i test Python e JS dalla tua macchina locale
(richiede Python e Node installati), oppure eseguirli dentro il container:

```bash
# Unit + integration test dentro il container backend
docker compose exec backend python -m pytest tests/ -v

# Coverage
docker compose exec backend pytest tests/ --cov=todo --cov-report=term-missing
```

> 💡 I test E2E Playwright vanno eseguiti dalla macchina locale puntando
> a `http://localhost:3000` (già configurato in `playwright.config.js`).

---
## 🚀 Setup locale (senza Docker)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py      # → http://localhost:5000

# Frontend
cd frontend
npm install
npx http-server src -p 3000   # → http://localhost:3000

# Playwright (prima volta)
npx playwright install --with-deps chromium
```

## 📋 Comandi di test

```bash
# Python
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/ --cov=todo --cov-report=term-missing --cov-fail-under=80
flake8 todo/ && black --check todo/

# JavaScript
npm test
npm run test:coverage
npm run lint

# E2E (con backend e frontend in esecuzione)
npx playwright test
npx playwright test --headed --slowMo=400   # debug
```

---

> 💡 **Regola d'oro:** non scrivere una sola riga di codice senza un test rosso che la giustifichi.
