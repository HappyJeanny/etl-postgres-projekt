-- Bundesland
CREATE TABLE bundesland (
    id_bundesland INT PRIMARY KEY,
    bundesland VARCHAR(50) NOT NULL
);

-- Filiale
CREATE TABLE filiale (
    id_filiale INT PRIMARY KEY,
    filiale VARCHAR(50) NOT NULL,
    id_bundesland INT NOT NULL REFERENCES bundesland(id_bundesland)
);

-- Kasse
CREATE TABLE kasse (
    id_kasse INT PRIMARY KEY,
    kassennr INT NOT NULL,
    id_filiale INT NOT NULL REFERENCES filiale(id_filiale)
);

-- Kategorie
CREATE TABLE kategorie (
    id_kategorie INT PRIMARY KEY,
    kategorie VARCHAR(50) NOT NULL
);

-- Lieferant
CREATE TABLE lieferant (
    id_lieferant INT PRIMARY KEY,
    lieferantenname VARCHAR(50) NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(10) CHECK (plz ~ '^[0-9]+$'),
    stadt VARCHAR(50),
    bundesland VARCHAR(50)
);

-- Artikel
CREATE TABLE artikel (
    id_artikel INT PRIMARY KEY,
    bezeichnung VARCHAR(50) NOT NULL,
    preis DECIMAL(10,2) NOT NULL CHECK (preis >= 0),
    id_kategorie INT NOT NULL REFERENCES kategorie(id_kategorie),
    id_lieferant INT NOT NULL REFERENCES lieferant(id_lieferant)
);

-- verkauft (Faktentabelle der operativen DB)
CREATE TABLE verkauft (
    id_verkauf INT PRIMARY KEY,
    id_kasse INT NOT NULL REFERENCES kasse(id_kasse),
    id_artikel INT NOT NULL REFERENCES artikel(id_artikel),
    menge INT NOT NULL CHECK (menge > 0),
    preis DECIMAL(10,2) NOT NULL CHECK (preis >= 0), -- Verkaufspreis zum Zeitpunkt
    datum_utc TIMESTAMP WITH TIME ZONE NOT NULL,
    datum_local TIMESTAMP WITHOUT TIME ZONE NOT NULL
);
