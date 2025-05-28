import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# .env laden
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# Verbindungsdaten
SRC_DB = os.getenv("DB_NAME")         # business_db
DWH_DB = os.getenv("DB_NAME_STAR")    # star-schema-db
USER = os.getenv("DB_USER")
PW = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

# Verbindungen aufbauen
src_conn = psycopg2.connect(
    dbname=SRC_DB, user=USER, password=PW, host=HOST, port=PORT
)
dwh_conn = psycopg2.connect(
    dbname=DWH_DB, user=USER, password=PW, host=HOST, port=PORT
)
src_cur = src_conn.cursor()
dwh_cur = dwh_conn.cursor()

# --- Dimensionen befüllen ---

# dim_bundesland
src_cur.execute("SELECT id_bundesland, bundesland FROM bundesland")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_bundesland (id_bundesland, bundesland) VALUES (%s, %s) ON CONFLICT DO NOTHING", row
    )

# dim_filiale
src_cur.execute("""
    SELECT f.id_filiale, f.filiale, b.bundesland
    FROM filiale f
    JOIN bundesland b ON f.id_bundesland = b.id_bundesland
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_filiale (id_filiale, filiale, bundesland) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", row
    )

# dim_lieferant
src_cur.execute("""
    SELECT id_lieferant, lieferantenname, strasse, plz, stadt, bundesland
    FROM lieferant
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_lieferant (id_lieferant, lieferantenname, strasse, plz, stadt, bundesland) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", row
    )

# dim_kategorie
src_cur.execute("SELECT id_kategorie, kategorie FROM kategorie")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_kategorie (id_kategorie, kategorie) VALUES (%s, %s) ON CONFLICT DO NOTHING", row
    )

# dim_artikel
src_cur.execute("""
    SELECT a.id_artikel, a.bezeichnung, k.kategorie
    FROM artikel a
    JOIN kategorie k ON a.id_kategorie = k.id_kategorie
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_artikel (id_artikel, bezeichnung, kategorie) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", row
    )

# dim_datum (aus verkauft generieren, falls nicht vorhanden)
src_cur.execute("SELECT DISTINCT datum_local FROM verkauft")
datum_set = set()
for (datum_local,) in src_cur.fetchall():
    datum = datum_local.date()
    if datum not in datum_set:
        jahr = datum.year
        monat = datum.month
        tag = datum.day
        wochentag = datum.strftime('%a')
        dwh_cur.execute(
            "INSERT INTO dim_datum (datum, jahr, monat, tag, wochentag) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (datum, jahr, monat, tag, wochentag)
        )
        datum_set.add(datum)

# Hilfsfunktion: Datum zu id_datum
def get_id_datum(datum, cur):
    cur.execute("SELECT id_datum FROM dim_datum WHERE datum = %s", (datum,))
    res = cur.fetchone()
    return res[0] if res else None

# --- Faktentabelle befüllen ---
src_cur.execute("""
    SELECT v.id_verkauf, v.id_kasse, v.id_artikel, v.menge, v.preis, v.datum_local,
           a.id_lieferant, k.id_filiale
    FROM verkauft v
    JOIN artikel a ON v.id_artikel = a.id_artikel
    JOIN kasse k ON v.id_kasse = k.id_kasse
""")
for row in src_cur.fetchall():
    id_verkauf, id_kasse, id_artikel, menge, preis, datum_local, id_lieferant, id_filiale = row
    umsatz = preis * menge
    datum = datum_local.date()
    id_datum = get_id_datum(datum, dwh_cur)
    dwh_cur.execute("""
        INSERT INTO fakt_verkauf
        (id_verkauf, id_datum, id_kasse, id_filiale, id_lieferant, id_artikel, menge, umsatz)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (id_verkauf, id_datum, id_kasse, id_filiale, id_lieferant, id_artikel, menge, umsatz))

# Commit und Verbindungen schließen
dwh_conn.commit()
src_cur.close()
dwh_cur.close()
src_conn.close()
dwh_conn.close()

print("ETL-Transfer abgeschlossen.")