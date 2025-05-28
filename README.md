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

- `init_db-docker.py`: Business-Datenbank initialisieren (Tabellen anlegen) 
-  in pgAdmin die Datenbank: `etl_db_star` anlegen
- `init_db-docker-star-schema.py`: DWH Datenbank initialisieren (Tabellen anlegen) 
-  den Inhalt von demo_data.sql in der SQL Query eingeben und ausführen
- ETL Prozess: xy.py ausführen (Daten werden von der etl_db in die etl_db_star verschoben)


`data/kunden.csv`: Rohdaten
- `data/kunden_bereinigt.csv`: bereinigte Daten

## ✅ Ziele

- Daten säubern
- Validieren
- In PostgreSQL importieren
- Docker & GitHub-ready
