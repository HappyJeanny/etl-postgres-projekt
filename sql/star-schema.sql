-- Alle löschen
/*
DROP TABLE IF EXISTS fakt_verkauf;
DROP TABLE IF EXISTS dim_artikel;
DROP TABLE IF EXISTS dim_kategorie;
DROP TABLE IF EXISTS dim_lieferant;
DROP TABLE IF EXISTS dim_filiale;
DROP TABLE IF EXISTS dim_bundesland;
DROP TABLE IF EXISTS dim_datum;
*/


-- Dimension: Lieferant
CREATE TABLE dim_lieferant (
    id_lieferant INT PRIMARY KEY,
    lieferantenname VARCHAR(50) NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(10),
    stadt VARCHAR(50),
    bundesland VARCHAR(50),
    valid_from DATE NOT NULL,
    valid_to DATE
);

-- Dimension: Artikel
CREATE TABLE dim_artikel (
    id_artikel INT PRIMARY KEY,
    bezeichnung VARCHAR(50) NOT NULL,
    kategorie VARCHAR(50) NOT NULL,
    preis DECIMAL(10,2) NOT NULL, 
    id_lieferant INT REFERENCES dim_lieferant(id_lieferant), 
    valid_from DATE NOT NULL,
    valid_to DATE    
);





-- Dimension: Filiale
CREATE TABLE dim_filiale (
    id_filiale INT PRIMARY KEY,
    filiale VARCHAR(50) NOT NULL,
    bundesland VARCHAR(50) NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE
);

-- Dimension: Kasse
CREATE TABLE dim_kasse (
    id_kasse INT PRIMARY KEY,
    kassennr INT NOT NULL,
    id_filiale INT REFERENCES dim_filiale(id_filiale),
    valid_from DATE NOT NULL,
    valid_to DATE
);


-- Dimension: Datum
CREATE TABLE dim_datum (
    id_datum SERIAL PRIMARY KEY,
    datum DATE NOT NULL,
    jahr INT,
    monat INT,
    tag INT,
    wochentag VARCHAR(10)
);

-- Faktentabelle: Verkäufe
CREATE TABLE fakt_verkauf (
    id_verkauf INT PRIMARY KEY,
    id_datum INT REFERENCES dim_datum(id_datum) ON DELETE SET NULL ON UPDATE CASCADE,
    id_kasse INT REFERENCES dim_kasse(id_kasse) ON DELETE SET NULL ON UPDATE CASCADE,
    id_filiale INT REFERENCES dim_filiale(id_filiale) ON DELETE SET NULL ON UPDATE CASCADE,    
    id_artikel INT NOT NULL REFERENCES dim_artikel(id_artikel) ON DELETE RESTRICT ON UPDATE CASCADE,
    preis DECIMAL(10,2) NOT NULL,
    menge INT NOT NULL,
    umsatz DECIMAL(10,2) NOT NULL,
    Datum_UTC TIMESTAMP WITH TIME ZONE NOT NULL,
    Datum_Lokal TIMESTAMP WITHOUT TIME ZONE NOT NULL
);