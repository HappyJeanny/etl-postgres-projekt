# ETL-Projekt mit Python, Pandas & PostgreSQL in Docker

## 🔧 Setup

1. `docker-compose up -d` starten
2. `.env` Datei anpassen
3. `etl_transform.py` ausführen
4. `import_to_db.py` ausführen

## 🐘 PostgreSQL Zugang

- Host: `localhost`
- Port: `5432`
- DB: `etl_db`
- User: `user`
- Passwort: `passwort123`

## 📁 Datenstruktur

- `data/kunden.csv`: Rohdaten
- `data/kunden_bereinigt.csv`: bereinigte Daten

## ✅ Ziele

- Daten säubern
- Validieren
- In PostgreSQL importieren
- Docker & GitHub-ready
