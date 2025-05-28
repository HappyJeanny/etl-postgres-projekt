-- Faktentabelle
CREATE TABLE fct_verkauf (
    id_verkauf INT PRIMARY KEY,
    datum_id INT REFERENCES dim_datum(datum_id),
    kasse_id INT REFERENCES dim_kasse(kasse_id),
    artikel_id INT REFERENCES dim_artikel(artikel_sk),
    menge INT,
    umsatz DECIMAL(10,2)
);

-- Dimension: Datum
CREATE TABLE dim_datum (
    datum_id INT PRIMARY KEY,
    datum DATE,
    tag INT,
    monat INT,
    jahr INT,
    wochentag_name VARCHAR(20),
    ist_wochenende BOOLEAN
);

-- Dimension: Kasse
CREATE TABLE dim_kasse (
    kasse_id INT PRIMARY KEY,
    id_kasse INT,
    kassen_nr INT,
    filiale_id INT,
    filiale VARCHAR(50),
    bundesland_id INT,
    bundesland VARCHAR(50)
);

-- Dimension: Artikel (SCD2)
CREATE TABLE dim_artikel (
    artikel_sk SERIAL PRIMARY KEY,
    id_artikel INT,
    bezeichnung VARCHAR(50),
    preis DECIMAL(10,2),
    id_kategorie INT,
    kategorie VARCHAR(50),
    id_lieferant INT,
    lieferantenname VARCHAR(50),
    gueltig_von DATE,
    gueltig_bis DATE,
    ist_aktuell BOOLEAN
);