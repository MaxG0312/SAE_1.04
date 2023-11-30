DROP TABLE IF EXISTS variete, culture, saison, parcelle, ticket_incident;

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
CREATE TABLE parcelle (
    id_parcelle INT AUTO_INCREMENT,
    surface DECIMAL(4,2),
    adresse VARCHAR(255),
    PRIMARY KEY(id_parcelle)
);

CREATE TABLE ticket_incident (
    id_ticket INT AUTO_INCREMENT,
    description_incident VARCHAR(255),
    date_incident DATETIME,
    statut_incident VARCHAR(31),
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

INSERT INTO ticket_incident VALUES
    (1, 'Incident 1', '2020-01-01 00:00:00', 'En cours'),
    (2, 'Incident 2', '2020-01-02 00:00:00', 'En cours'),
    (3, 'Incident 3', '2020-01-03 00:00:00', 'En cours'),
    (4, 'Incident 4', '2020-01-04 00:00:00', 'En cours'),
    (5, 'Incident 5', '2020-01-05 00:00:00', 'En cours'),
    (6, 'Incident 6', '2020-01-06 00:00:00', 'En cours');
INSERT INTO parcelle VALUES 
    (1, 2.5, '1 rue de la Paix'),
    (2, 1.5, '2 rue de la Paix'),
    (3, 3.5, '3 rue de la Paix'),
    (4, 4.5, '4 rue de la Paix'),
    (5, 5.5, '5 rue de la Paix'),
    (6, 6.5, '6 rue de la Paix');
