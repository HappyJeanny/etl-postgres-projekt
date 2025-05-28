import psycopg2
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

def execute_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql = file.read()
    return sql

def main():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            # Beispiel: SQL-Datei ausführen (optional)
            sql_path = os.path.join(os.path.dirname(__file__), "..", "sql", "business_db.sql")
            sql = execute_sql(sql_path)            
            cur.execute(sql)
            print("Business-DB erfolgreich erstellt.")
    except Exception as e:
        print("Fehler beim Verbinden oder Ausführen:", e)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()