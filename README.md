# ETL-Projekt mit Python, Pandas & PostgreSQL in Docker

## 🔧 Setup

1. `docker-compose up -d` starten
2. `.env` Datei anpassen
3. `init_db-docker.py` ausführen
4. ` ` ausführen

## 🐘 PostgreSQL Zugang

- Host: `localhost`
- Port: `5436`
- DB: `etl_db`
- User: `user`
- Passwort: `passwort123`

## 📁 Datenstruktur

- sql/business_db.sql : Datenbank initialisieren (Tabellen anlegen)
- 
`data/kunden.csv`: Rohdaten
- `data/kunden_bereinigt.csv`: bereinigte Daten

## ✅ Ziele

- Daten säubern
- Validieren
- In PostgreSQL importieren
- Docker & GitHub-ready
