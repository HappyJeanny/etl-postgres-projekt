import pandas as pd

# CSV laden
df = pd.read_csv("data/kunden.csv")

# Whitespace in allen String-Spalten entfernen
for col in df.select_dtypes(include=["object"]):
    df[col] = df[col].str.strip()

# E-Mails in Kleinbuchstaben
df["email"] = df["email"].str.lower()

# Alter bereinigen
def valid_age(x):
    try:
        x = int(x)
        return x if x >= 0 else None
    except:
        return None

df["alter"] = df["alter"].apply(valid_age)

# Ungültige Zeilen entfernen
df_cleaned = df.dropna(subset=["email", "alter"])

# Speichern (optional)
df_cleaned.to_csv("data/kunden_bereinigt.csv", index=False)

print(df_cleaned)

