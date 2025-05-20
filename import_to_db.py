import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# .env laden
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, encoding='utf-8')

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Daten laden
csv_path = os.path.join("data", "kunden_bereinigt.csv")
df = pd.read_csv(csv_path)

# Verbindung
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS kunden")

# Tabelle mit E-Mail als UNIQUE-Schlüssel
cursor.execute("""
CREATE TABLE IF NOT EXISTS kunden (
    name TEXT,
    email TEXT UNIQUE,
    alter INT
)
""")

# Duplikatprüfung per ON CONFLICT
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO kunden (name, email, alter)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING
        """,
        (row["name"], row["email"], int(row["alter"]))
    )

conn.commit()
cursor.close()
conn.close()

print("✅ CSV-Daten importiert – Duplikate wurden übersprungen.")
