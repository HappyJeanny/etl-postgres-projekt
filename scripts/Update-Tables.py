"""
Dieses Skript erzeugt neue Demo-Daten für die Business-DB (analog zu demo_data.sql)
und schreibt sie als SQL-Insert-Statements in eine neue Datei (z.B. new_demo_data.sql).
"""

import random
from datetime import datetime, timedelta

# Hilfsdaten
bundeslaender = [
    (6, 'Baden-Württemberg'),
    (7, 'Niedersachsen'),
]
filialen = [
    (6, 'Filiale Stuttgart', 6),
    (7, 'Filiale Hannover', 7),
]
kassen = [
    (6, 501, 6),
    (7, 601, 7),
]
kategorien = [
    (6, 'Süßwaren'),
    (7, 'Tiefkühlkost'),
]
lieferanten = [
    (6, 'Süßwaren GmbH', 'Süßstr. 6', '70173', 'Stuttgart', 'Baden-Württemberg'),
    (7, 'TK AG', 'Frostweg 7', '30159', 'Hannover', 'Niedersachsen'),
]
artikel = [
    (6, 'Schokolade', 1.49, 6, 6),
    (7, 'Pizza TK', 2.99, 7, 7),
]

# Neue Verkäufe generieren (z.B. für die letzten 5 Tage)
verkauft = []
base_date = datetime.now() - timedelta(days=5)
for i in range(11, 21):
    tag_offset = random.randint(0, 4)
    stunde = random.randint(8, 18)
    minute = random.randint(0, 59)
    datum = base_date + timedelta(days=tag_offset, hours=stunde, minutes=minute)
    id_kasse = random.choice([6, 7])
    id_artikel = random.choice([6, 7])
    menge = random.randint(1, 5)
    preis = [a[2] for a in artikel if a[0] == id_artikel][0]
    umsatz = round(preis * menge, 2)
    verkauft.append(
        (i, id_kasse, id_artikel, menge, umsatz, datum.strftime('%Y-%m-%d %H:%M:%S+02'), datum.strftime('%Y-%m-%d %H:%M:%S'))
    )

# SQL-Datei schreiben
with open("new_demo_data.sql", "w", encoding="utf-8") as f:
    # Bundesland
    f.write("-- Neue Bundesländer\n")
    for b in bundeslaender:
        f.write(f"INSERT INTO bundesland VALUES ({b[0]}, '{b[1]}');\n")
    f.write("\n")
    # Filiale
    f.write("-- Neue Filialen\n")
    for fil in filialen:
        f.write(f"INSERT INTO filiale VALUES ({fil[0]}, '{fil[1]}', {fil[2]});\n")
    f.write("\n")
    # Kasse
    f.write("-- Neue Kassen\n")
    for k in kassen:
        f.write(f"INSERT INTO kasse VALUES ({k[0]}, {k[1]}, {k[2]});\n")
    f.write("\n")
    # Kategorie
    f.write("-- Neue Kategorien\n")
    for kat in kategorien:
        f.write(f"INSERT INTO kategorie VALUES ({kat[0]}, '{kat[1]}');\n")
    f.write("\n")
    # Lieferant
    f.write("-- Neue Lieferanten\n")
    for l in lieferanten:
        f.write(f"INSERT INTO lieferant VALUES ({l[0]}, '{l[1]}', '{l[2]}', '{l[3]}', '{l[4]}', '{l[5]}');\n")
    f.write("\n")
    # Artikel
    f.write("-- Neue Artikel\n")
    for a in artikel:
        f.write(f"INSERT INTO artikel VALUES ({a[0]}, '{a[1]}', {a[2]}, {a[3]}, {a[4]});\n")
    f.write("\n")
    # Verkäufe
    f.write("-- Neue Verkäufe\n")
    for v in verkauft:
        f.write(f"INSERT INTO verkauft VALUES ({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, '{v[5]}', '{v[6]}');\n")

print("Neue Demo-Daten wurden in new_demo_data.sql geschrieben.")