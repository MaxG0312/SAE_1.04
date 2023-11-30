DROP TABLE IF EXISTS variete, culture, saison, ticket_incident;

CREATE TABLE saison (
    saison VARCHAR(31),
    PRIMARY KEY(saison)
);

CREATE TABLE culture (
    id_culture INT AUTO_INCREMENT,
    libelle_culture VARCHAR(255),
    PRIMARY KEY(id_culture)
);

CREATE TABLE variete (
    id_variete INT AUTO_INCREMENT,
    libelle_variete VARCHAR(255),
    saison VARCHAR(31),
    culture INT,
    prix_kg DECIMAL(4,2),
    stock DECIMAL(4,1),
    PRIMARY KEY(id_variete),
    FOREIGN KEY(saison) REFERENCES saison(saison),
    FOREIGN KEY(culture) REFERENCES culture(id_culture)
);

CREATE TABLE ticket_incident (
    id_ticket INT AUTO_INCREMENT,
    description VARCHAR(255),
    date_ticket DATETIME,
    statut VARCHAR(31),
    PRIMARY KEY(id_ticket)
);

INSERT INTO saison VALUES
   ('Printemps'),
   ('Ete'),
   ('Automne'),
   ('Hiver');

INSERT INTO culture VALUES
    (1, 'Tomates'),
    (2, 'Pommes'),
    (3, 'Poires'),
    (4, 'Maïs'),
    (5, 'Blé'),
    (6, 'Carottes');

INSERT INTO variete VALUES
    (1, 'Carottes de Nantes', 'Ete', 6, 1.5, 74.5),
    (2, 'Tomates cerises', 'Ete', 1, 5.67, 52.0),
    (3, 'Pommes Gala', 'Hiver', 2, 1.95, 0),
    (4, 'Poires Williams', 'Ete', 3, 3.99, 5.8);
