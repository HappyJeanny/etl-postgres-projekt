"""
Dieses Skript überträgt neue/aktualisierte Datensätze aus der etl_db (Business-DB) in das Data Warehouse (etl_db_star).
Bei Änderungen werden die alten SCD2-Datensätze mit valid_to geschlossen und neue Versionen eingefügt.
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Logging konfigurieren
log_path = os.path.join(os.path.dirname(__file__), "etl_transfer_update.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_now():
    return datetime.now().date()

def update_dim_scd2(src_cur, dwh_cur, src_table, dwh_table, key_col, attrib_cols):
    src_cur.execute(f"SELECT {', '.join([key_col] + attrib_cols)} FROM {src_table}")
    src_rows = src_cur.fetchall()
    added, updated, unchanged = 0, 0, 0
    for row in src_rows:
        key = row[0]
        attribs = row[1:]
        dwh_cur.execute(
            f"SELECT {', '.join(attrib_cols)}, valid_from, valid_to FROM {dwh_table} WHERE {key_col} = %s AND valid_to IS NULL",
            (key,)
        )
        dwh_row = dwh_cur.fetchone()
        if dwh_row is None:
            dwh_cur.execute(
                f"INSERT INTO {dwh_table} ({key_col}, {', '.join(attrib_cols)}, valid_from, valid_to) VALUES ({', '.join(['%s']*(len(row)))}, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"INSERT {dwh_table}: {key_col}={key}, Werte={attribs}")
            added += 1
        elif dwh_row[:-2] != attribs:
            dwh_cur.execute(
                f"UPDATE {dwh_table} SET valid_to = %s WHERE {key_col} = %s AND valid_to IS NULL",
                (get_now(), key)
            )
            dwh_cur.execute(
                f"INSERT INTO {dwh_table} ({key_col}, {', '.join(attrib_cols)}, valid_from, valid_to) VALUES ({', '.join(['%s']*(len(row)))}, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"UPDATE {dwh_table}: {key_col}={key}, alte Werte={dwh_row[:-2]}, neue Werte={attribs}")
            updated += 1
        else:
            unchanged += 1
    logging.info(f"{dwh_table}: {added} neue, {updated} geänderte, {unchanged} unveränderte Datensätze verarbeitet.")

def update_dim_artikel_scd2(src_cur, dwh_cur):
    src_cur.execute("""
        SELECT a.id_artikel, a.bezeichnung, k.kategorie, a.preis, a.id_lieferant
        FROM artikel a
        JOIN kategorie k ON a.id_kategorie = k.id_kategorie
    """)
    src_rows = src_cur.fetchall()
    added, updated, unchanged = 0, 0, 0
    for row in src_rows:
        key = row[0]
        attribs = row[1:]
        dwh_cur.execute(
            "SELECT bezeichnung, kategorie, preis, id_lieferant, valid_from, valid_to FROM dim_artikel WHERE id_artikel = %s AND valid_to IS NULL",
            (key,)
        )
        dwh_row = dwh_cur.fetchone()
        if dwh_row is None:
            dwh_cur.execute(
                "INSERT INTO dim_artikel (id_artikel, bezeichnung, kategorie, preis, id_lieferant, valid_from, valid_to) VALUES (%s, %s, %s, %s, %s, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"INSERT dim_artikel: id_artikel={key}, Werte={attribs}")
            added += 1
        elif dwh_row[:-2] != attribs:
            dwh_cur.execute(
                "UPDATE dim_artikel SET valid_to = %s WHERE id_artikel = %s AND valid_to IS NULL",
                (get_now(), key)
            )
            dwh_cur.execute(
                "INSERT INTO dim_artikel (id_artikel, bezeichnung, kategorie, preis, id_lieferant, valid_from, valid_to) VALUES (%s, %s, %s, %s, %s, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"UPDATE dim_artikel: id_artikel={key}, alte Werte={dwh_row[:-2]}, neue Werte={attribs}")
            updated += 1
        else:
            unchanged += 1
    logging.info(f"dim_artikel: {added} neue, {updated} geänderte, {unchanged} unveränderte Datensätze verarbeitet.")

def update_dim_filiale_scd2(src_cur, dwh_cur):
    src_cur.execute("""
        SELECT f.id_filiale, f.filiale, b.bundesland
        FROM filiale f
        JOIN bundesland b ON f.id_bundesland = b.id_bundesland
    """)
    src_rows = src_cur.fetchall()
    added, updated, unchanged = 0, 0, 0
    for row in src_rows:
        key = row[0]
        attribs = row[1:]
        dwh_cur.execute(
            "SELECT filiale, bundesland, valid_from, valid_to FROM dim_filiale WHERE id_filiale = %s AND valid_to IS NULL",
            (key,)
        )
        dwh_row = dwh_cur.fetchone()
        if dwh_row is None:
            dwh_cur.execute(
                "INSERT INTO dim_filiale (id_filiale, filiale, bundesland, valid_from, valid_to) VALUES (%s, %s, %s, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"INSERT dim_filiale: id_filiale={key}, Werte={attribs}")
            added += 1
        elif dwh_row[:-2] != attribs:
            dwh_cur.execute(
                "UPDATE dim_filiale SET valid_to = %s WHERE id_filiale = %s AND valid_to IS NULL",
                (get_now(), key)
            )
            dwh_cur.execute(
                "INSERT INTO dim_filiale (id_filiale, filiale, bundesland, valid_from, valid_to) VALUES (%s, %s, %s, %s, NULL)",
                (*row, get_now())
            )
            logging.info(f"UPDATE dim_filiale: id_filiale={key}, alte Werte={dwh_row[:-2]}, neue Werte={attribs}")
            updated += 1
        else:
            unchanged += 1
    logging.info(f"dim_filiale: {added} neue, {updated} geänderte, {unchanged} unveränderte Datensätze verarbeitet.")

def update_fakt_verkauf(src_cur, dwh_cur, get_id_datum):
    src_cur.execute("""
        SELECT 
            v.id_verkauf, v.id_kasse, v.id_artikel, v.menge, v.preis, 
            v.preis * v.menge AS umsatz, v.datum_utc, v.datum_local, k.id_filiale
        FROM verkauft v
        JOIN kasse k ON v.id_kasse = k.id_kasse
    """)
    for row in src_cur.fetchall():
        datum = row[7].date()
        id_datum = get_id_datum(datum, dwh_cur)
        dwh_cur.execute("""
            INSERT INTO fakt_verkauf (
                id_verkauf, id_datum, id_kasse, id_filiale, id_artikel, preis, menge, umsatz, Datum_UTC, Datum_Lokal
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            row[0], id_datum, row[1], row[8], row[2], row[4], row[3], row[5], row[6], row[7]
        ))

def get_id_datum(datum, cur):
    cur.execute("SELECT id_datum FROM dim_datum WHERE datum = %s", (datum,))
    res = cur.fetchone()
    return res[0] if res else None

def main():
    # Load .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"The .env file was not found at the expected path: {dotenv_path}")
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

    src_conn = psycopg2.connect(dbname=SRC_DB, user=USER, password=PW, host=HOST, port=PORT)
    dwh_conn = psycopg2.connect(dbname=DWH_DB, user=USER, password=PW, host=HOST, port=PORT)
    src_cur = src_conn.cursor()
    dwh_cur = dwh_conn.cursor()

    update_dim_scd2(src_cur, dwh_cur, "lieferant", "dim_lieferant", "id_lieferant", ["lieferantenname", "strasse", "plz", "stadt", "bundesland"])
    update_dim_artikel_scd2(src_cur, dwh_cur)
    update_dim_filiale_scd2(src_cur, dwh_cur)
    update_dim_scd2(src_cur, dwh_cur, "kasse", "dim_kasse", "id_kasse", ["kassennr", "id_filiale"])
    update_fakt_verkauf(src_cur, dwh_cur, get_id_datum)

    dwh_conn.commit()
    src_cur.close()
    dwh_cur.close()
    src_conn.close()
    dwh_conn.close()
    logging.info("SCD2-Update abgeschlossen.")
    print("SCD2-Update abgeschlossen.")

if __name__ == "__main__":
    main()