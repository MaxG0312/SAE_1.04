DROP TABLE IF EXISTS Saison, Culture, Variete;

CREATE TABLE Saison (
    saison VARCHAR(31),
    PRIMARY KEY(saison)
);

CREATE TABLE Culture (
    id_culture INT AUTO_INCREMENT,
    libelle_culture VARCHAR(255),
    PRIMARY KEY(id_culture)
);

CREATE TABLE Variete (
    id_variete INT AUTO_INCREMENT,
    libelle_variete VARCHAR(255),
    saison VARCHAR(31),
    culture INT,
    prix_kg DOUBLE,
    PRIMARY KEY(id_variete),
    FOREIGN KEY(saison) REFERENCES Saison(saison),
    FOREIGN KEY(culture) REFERENCES Culture(id_culture)
);

INSERT INTO Saison VALUES
   ('Printemps'),
   ('Ete'),
   ('Automne'),
   ('Hiver');

INSERT INTO Culture VALUES
    (1, 'Tomates'),
    (2, 'Pommes'),
    (3, 'Poires'),
    (4, 'Maïs'),
    (5, 'Blé'),
    (6, 'Carottes');

INSERT INTO Variete VALUES
    (1, 'Carottes de Nantes', 'Ete', 6, 1.5),
    (2, 'Tomates cerises', 'Ete', 1, 5.67),
    (3, 'Pommes Gala', 'Hiver', 2, 1.95),
    (4, 'Poires Williams', 'Ete', 3, 3.99);