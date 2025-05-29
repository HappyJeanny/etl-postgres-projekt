-- Neue Bundesländer
INSERT INTO bundesland VALUES (6, 'Baden-Württemberg');
INSERT INTO bundesland VALUES (7, 'Niedersachsen');

-- Neue Filialen
INSERT INTO filiale VALUES (6, 'Filiale Stuttgart', 6);
INSERT INTO filiale VALUES (7, 'Filiale Hannover', 7);

-- Neue Kassen
INSERT INTO kasse VALUES (6, 501, 6);
INSERT INTO kasse VALUES (7, 601, 7);

-- Neue Kategorien
INSERT INTO kategorie VALUES (6, 'Süßwaren');
INSERT INTO kategorie VALUES (7, 'Tiefkühlkost');

-- Neue Lieferanten
INSERT INTO lieferant VALUES (6, 'Süßwaren GmbH', 'Süßstr. 6', '70173', 'Stuttgart', 'Baden-Württemberg');
INSERT INTO lieferant VALUES (7, 'TK AG', 'Frostweg 7', '30159', 'Hannover', 'Niedersachsen');

-- Neue Artikel
INSERT INTO artikel VALUES (6, 'Schokolade', 1.49, 6, 6);
INSERT INTO artikel VALUES (7, 'Pizza TK', 2.99, 7, 7);

-- Neue Verkäufe
INSERT INTO verkauft VALUES (11, 7, 7, 4, 11.96, '2025-05-26 08:20:31+02', '2025-05-26 08:20:31');
INSERT INTO verkauft VALUES (12, 6, 6, 4, 5.96, '2025-05-28 03:36:31+02', '2025-05-28 03:36:31');
INSERT INTO verkauft VALUES (13, 7, 7, 2, 5.98, '2025-05-28 09:05:31+02', '2025-05-28 09:05:31');
INSERT INTO verkauft VALUES (14, 7, 7, 5, 14.95, '2025-05-28 09:09:31+02', '2025-05-28 09:09:31');
INSERT INTO verkauft VALUES (15, 6, 7, 1, 2.99, '2025-05-29 00:06:31+02', '2025-05-29 00:06:31');
INSERT INTO verkauft VALUES (16, 7, 7, 1, 2.99, '2025-05-25 04:57:31+02', '2025-05-25 04:57:31');
INSERT INTO verkauft VALUES (17, 7, 6, 1, 1.49, '2025-05-29 00:27:31+02', '2025-05-29 00:27:31');
INSERT INTO verkauft VALUES (18, 6, 6, 3, 4.47, '2025-05-27 23:51:31+02', '2025-05-27 23:51:31');
INSERT INTO verkauft VALUES (19, 7, 6, 3, 4.47, '2025-05-28 09:19:31+02', '2025-05-28 09:19:31');
INSERT INTO verkauft VALUES (20, 6, 6, 3, 4.47, '2025-05-28 08:52:31+02', '2025-05-28 08:52:31');
