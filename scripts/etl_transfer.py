import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

now = datetime.now().date()  # oder datetime.now() für Timestamp


# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"The .env file was not found at the expected path: {dotenv_path}")
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path, encoding='utf-8')

# Überprüfen, ob alle benötigten Umgebungsvariablen gesetzt sind
required_vars = ["DB_NAME", "DB_NAME_STAR", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Verbindungsdaten
SRC_DB = os.getenv("DB_NAME")         # business_db
DWH_DB = os.getenv("DB_NAME_STAR")    # star-schema-db
USER = os.getenv("DB_USER")
PW = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

# Verbindungen aufbauen
def new_func(SRC_DB, USER, PW, HOST, PORT):
    src_conn = psycopg2.connect(
    dbname=SRC_DB, user=USER, password=PW, host=HOST, port=PORT
)
    
    return src_conn

src_conn = new_func(SRC_DB, USER, PW, HOST, PORT)
dwh_conn = psycopg2.connect(
    dbname=DWH_DB, user=USER, password=PW, host=HOST, port=PORT
)
src_cur = src_conn.cursor()
dwh_cur = dwh_conn.cursor()

# --- Dimensionen befüllen ---

#dim_filiale
src_cur.execute("""
    SELECT f.id_filiale, f.filiale, b.bundesland 
    FROM filiale f
    JOIN bundesland b ON f.id_bundesland = b.id_bundesland
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_filiale (id_filiale, filiale, bundesland, valid_from, valid_to) VALUES (%s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING",
        (row[0], row[1], row[2], now)
    )




# dim_kasse
src_cur.execute("""
    SELECT id_kasse, kassennr, id_filiale
    FROM kasse
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_kasse (id_kasse, kassennr, id_filiale, valid_from, valid_to) VALUES (%s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING",
        (row[0], row[1], row[2], now)
    )





# dim_lieferant
# dim_lieferant
src_cur.execute("""
    SELECT id_lieferant, lieferantenname, strasse, plz, stadt, bundesland
    FROM lieferant
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_lieferant (id_lieferant, lieferantenname, strasse, plz, stadt, bundesland, valid_from, valid_to) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING",
        (row[0], row[1], row[2], row[3], row[4], row[5], now)
    )



# dim_artikel
# dim_artikel
src_cur.execute("""
    SELECT a.id_artikel, a.bezeichnung, k.kategorie, a.preis, a.id_lieferant
    FROM artikel a
    JOIN kategorie k ON a.id_kategorie = k.id_kategorie
""")
for row in src_cur.fetchall():
    dwh_cur.execute(
        "INSERT INTO dim_artikel (id_artikel, bezeichnung, kategorie, preis, id_lieferant, valid_from, valid_to) VALUES (%s, %s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING",
        (row[0], row[1], row[2], row[3], row[4], now)
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

# Faktentabelle: Verkäufe
src_cur.execute("""
    SELECT 
        v.id_verkauf, 
        v.id_kasse, 
        v.id_artikel, 
        v.menge, 
        v.preis, 
        v.preis * v.menge AS umsatz, 
        v.datum_utc, 
        v.datum_local,
        k.id_filiale
    FROM verkauft v
    JOIN artikel a ON v.id_artikel = a.id_artikel
    JOIN kasse k ON v.id_kasse = k.id_kasse
    
""")
for row in src_cur.fetchall():
    # Hole das Datum für die Zeitdimension
    datum = row[7].date()  # row[7] = datum_local
    id_datum = get_id_datum(datum, dwh_cur)
    dwh_cur.execute("""
        INSERT INTO fakt_verkauf (
            id_verkauf, id_datum, id_kasse, id_filiale, id_artikel, preis, menge, umsatz, Datum_UTC, Datum_Lokal
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (
        row[0],                # id_verkauf
        id_datum,              # id_datum (aus dim_datum)
        row[1],                # id_kasse
        row[8],                # id_filiale 
        row[2],                # id_artikel
        row[4],                # preis
        row[3],                # menge
        row[5],                # umsatz
        row[6],                # Datum_UTC
        row[7]                 # Datum_Lokal
    ))




# Commit und Verbindungen schließen
dwh_conn.commit()
src_cur.close()
dwh_cur.close()
src_conn.close()
dwh_conn.close()

print("ETL-Transfer abgeschlossen.")