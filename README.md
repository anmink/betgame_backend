# backend_betgame

REST-API-Backend für ein Sport-Wettspiel — Spieler können anstehende Fußballspiele durchsuchen, auf Ergebnisse wetten und ihren Kontostand sowie ihre Wetthistorie einsehen.

Entwickelt als persönliches Fullstack-Projekt, um Python-Backend-Entwicklung, PostgreSQL via Supabase sowie CI/CD mit GitHub Actions in der Praxis anzuwenden.

---

## Tech Stack

| Bereich | Technologie |
|---|---|
| Framework | FastAPI |
| Datenbank | PostgreSQL via Supabase |
| Authentifizierung | JWT (PyJWT) |
| Geplante Aufgaben | APScheduler |
| Tests | pytest, pytest-mock |
| Laufzeit | uvicorn |
| Containerisierung | Docker |
| CI/CD | GitHub Actions |

---

## Features

- **Authentifizierung** — JWT-basierter Login und Token-Validierung
- **Spieldaten** — Fußball-Fixtures mit aktuellen Quoten aus einer externen API
- **Wetten** — Einsätze auf Heimsieg, Unentschieden oder Auswärtssieg
- **Kontoverwaltung** — Guthaben wird nach Spielauflösung automatisch aktualisiert
- **Automatische Updates** — APScheduler ruft Spielergebnisse ab und schließt offene Wetten planmäßig ab
- **REST-API** — Saubere Endpunkt-Struktur, dokumentiert über FastAPIs automatisch generierte Swagger-Oberfläche

---

## Projektstruktur

```
backend_betgame/
├── app/
│   ├── main.py          # FastAPI App-Einstiegspunkt
│   ├── routers/         # Endpunkt-Definitionen (auth, matches, bets)
│   ├── models/          # Pydantic-Schemas
│   ├── services/        # Geschäftslogik
│   └── scheduler.py     # APScheduler-Job-Definitionen
├── .env                 # Umgebungsvariablen (nicht eingecheckt)
├── requirements.txt
└── Dockerfile
```

---

## Schnellstart

### Voraussetzungen

- Python 3.11+
- Ein Supabase-Projekt (kostenlose Stufe reicht)

### Lokale Einrichtung

```bash
# Repository klonen
git clone https://github.com/anmink/backend_betgame.git
cd backend_betgame

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# .env-Datei anlegen und befüllen
cp .env.example .env

# Server starten
uvicorn app.main:app --reload
```

Die API ist erreichbar unter `http://localhost:8000`.  
Interaktive Dokumentation: `http://localhost:8000/docs`

### Mit Docker

```bash
docker build -t betgame-backend .
docker run -p 8000:8000 --env-file .env betgame-backend
```

---

## Umgebungsvariablen

```env
SUPABASE_URL=deine_supabase_projekt_url
SUPABASE_KEY=dein_supabase_anon_key
JWT_SECRET=dein_jwt_secret
```

---

## Tests ausführen

```bash
pytest tests/ -v
```

---

## CI/CD

Jeder Push auf `main` löst eine GitHub Actions Pipeline aus, die:

1. Alle pytest-Tests ausführt
2. Das Docker-Image baut (nur bei grünen Tests)

---

## Status

In aktiver Entwicklung — Teil eines größeren Betgame-Projekts mit einem Vue 3 + TypeScript Web-Frontend.
