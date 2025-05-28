-- Bundesland
INSERT INTO bundesland VALUES
  (1, 'Bayern'),
  (2, 'Berlin'),
  (3, 'Hamburg'),
  (4, 'Sachsen'),
  (5, 'Hessen');

-- Filiale
INSERT INTO filiale VALUES
  (1, 'Filiale München', 1),
  (2, 'Filiale Berlin', 2),
  (3, 'Filiale Hamburg', 3),
  (4, 'Filiale Dresden', 4),
  (5, 'Filiale Frankfurt', 5);

-- Kasse
INSERT INTO kasse VALUES
  (1, 101, 1),
  (2, 102, 1),
  (3, 201, 2),
  (4, 301, 3),
  (5, 401, 4);

-- Kategorie
INSERT INTO kategorie VALUES
  (1, 'Getränke'),
  (2, 'Snacks'),
  (3, 'Obst'),
  (4, 'Milchprodukte'),
  (5, 'Backwaren');

-- Lieferant
INSERT INTO lieferant VALUES
  (1, 'Getränke GmbH', 'Hauptstr. 1', '80331', 'München', 'Bayern'),
  (2, 'Snack AG', 'Snackweg 2', '10115', 'Berlin', 'Berlin'),
  (3, 'Obsthandel', 'Obstallee 3', '20095', 'Hamburg', 'Hamburg'),
  (4, 'Milchhof', 'Milchstr. 4', '01067', 'Dresden', 'Sachsen'),
  (5, 'Bäckerei', 'Brotweg 5', '60311', 'Frankfurt', 'Hessen');

-- Artikel
INSERT INTO artikel VALUES
  (1, 'Cola 1L', 1.29, 1, 1),
  (2, 'Chips Paprika', 1.99, 2, 2),
  (3, 'Apfel', 0.49, 3, 3),
  (4, 'Milch 1L', 0.89, 4, 4),
  (5, 'Brötchen', 0.35, 5, 5);

-- verkauft (10 Datensätze)
INSERT INTO verkauft VALUES
  (1, 1, 1, 2, 2.58, '2024-05-01 08:15:00+02', '2024-05-01 08:15:00'),
  (2, 2, 2, 1, 1.99, '2024-05-01 09:00:00+02', '2024-05-01 09:00:00'),
  (3, 3, 3, 5, 2.45, '2024-05-01 10:30:00+02', '2024-05-01 10:30:00'),
  (4, 4, 4, 3, 2.67, '2024-05-02 11:00:00+02', '2024-05-02 11:00:00'),
  (5, 5, 5, 10, 3.50, '2024-05-02 12:00:00+02', '2024-05-02 12:00:00'),
  (6, 1, 2, 3, 5.97, '2024-05-03 13:00:00+02', '2024-05-03 13:00:00'),
  (7, 2, 3, 2, 0.98, '2024-05-03 14:00:00+02', '2024-05-03 14:00:00'),
  (8, 3, 4, 1, 0.89, '2024-05-04 15:00:00+02', '2024-05-04 15:00:00'),
  (9, 4, 5, 4, 1.40, '2024-05-04 16:00:00+02', '2024-05-04 16:00:00'),
  (10, 5, 1, 6, 7.74, '2024-05-05 17:00:00+02', '2024-05-05 17:00:00');