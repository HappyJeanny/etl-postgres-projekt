# Projektpräsentation: Data-Warehouse für Handelsunternehmen

## 1. Name des Projekts

**"Data-Warehouse Lidl"**

## 2. Teammitglieder

* Isabell Mader

## 3. Einschränkungen / Randbedingungen

* Ein Produkt kann nur einem Lieferanten zugeordnet sein.
* Jede Filiale befindet sich in genau einem Bundesland.
* Verkäufe erfolgen ausschließlich über registrierte Kassen.

## 4. Business DB – Design (ER)

* Strukturierte 3NF-Datenbank mit Tabellen für Filialen, Kassen, Artikel, Lieferanten etc.
* **ER-Modell** ist in `er-modell.svg` enthalten

## 5. DWH Design (Starschema)

* Faktentabelle: `fakt_verkauf`
* Dimensionstabellen: `dim_artikel`, `dim_kasse`, `dim_filiale`, `dim_lieferant`, `dim_datum`
* **Diagramm**: enthalten in `index.html`

## 6. SCD-Varianten

* Verwendet: **SCD Type 2** (Historisierung in `dim_artikel`, `dim_lieferant`, etc.)
* Neue Gültigkeitseinträge bei Änderung der Quelldaten

## 7. Schedule von ETL

* Initialer Load durch `etl_transfer.py`
* Updates via `etl_transfer-update.py`
* Triggerung manuell bzw. cronjob-fähig (optional mit Airflow erweiterbar)

## 8. Was habe ich gelernt?

* Einsatz von Star-Schema zur performanten Analyse
* Umgang mit SCD2 zur Historisierung
* Anwendung von Python, Pandas, PostgreSQL und Docker
* Gute Strukturierung und Versionierung via GitHub

## 9. Highlights

* Vollständig dockerisierter Stack
* Sauber dokumentierter ETL-Prozess
* Zeitdimension automatisch generiert aus Verkaufsdaten
* Automatisches Update-Skript für neue Datensätze

## 10. Probleme + Lösungen

* **Problem**: Initial fehlende Zeitdimension führte zu JOIN-Fehlern

  * **Lösung**: Generierung direkt aus `verkauft.datum_local`
* **Problem**: Duplicate Keys beim Nachladen

  * **Lösung**: `ON CONFLICT DO NOTHING` in Insert-Statements

## 11. Tipps für Kollegen

* ETL Schritt für Schritt testen, bevor alles automatisiert wird
* Immer mit Beispieldaten starten, um Modell zu validieren
* Validierungsregeln für ETL früh definieren (z. B. bei PLZ, Preis, etc.)
* .env sauber strukturieren und nicht in GitHub hochladen

---

*Optional: Screenshots aus pgAdmin oder Diagramme aus draw\.io ergänzen.*
