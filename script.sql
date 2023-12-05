DROP TABLE IF EXISTS collecte, ticket_incident, variete, parcelle, culture, saison;

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
    stock DECIMAL(4,2),
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
    date_incident DATE,
    statut_incident VARCHAR(31),
    parcelle_concernee INT,
    PRIMARY KEY(id_ticket),
    FOREIGN KEY(parcelle_concernee) REFERENCES parcelle(id_parcelle)
);

CREATE TABLE collecte(
   id_collecte INT AUTO_INCREMENT,
   quantite_collecte DOUBLE,
   produit_collecte VARCHAR(50),
   date_collecte DATETIME,
   id_parcelle INT NOT NULL,
   PRIMARY KEY(id_collecte) ,
   FOREIGN KEY(id_parcelle) REFERENCES parcelle(id_parcelle)
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

INSERT INTO parcelle VALUES 
    (1, 23.5, '1 rue de la Paix'),
    (2, 17.5, '2 rue de la Paix'),
    (3, 45.5, '3 rue de la Paix'),
    (4, 4.5, '4 rue de la Paix'),
    (5, 5.5, '5 rue de la Paix'),
    (6, 6.5, '6 rue de la Paix');

INSERT INTO ticket_incident VALUES
    (NULL, 'Incendie', '2020-09-27', 'En cours', 1),
    (NULL, 'Inondation', '2020-09-27', 'En cours', 2),
    (NULL, 'Incendie', '2020-09-27', 'En cours', 3),
    (NULL, 'Inondation', '2020-09-27', 'En cours', 4),
    (NULL, 'Incendie', '2020-09-27', 'En cours', 5),
    (NULL, 'Inondation', '2020-09-27', 'En cours', 6);
    

INSERT INTO collecte VALUES (1, 23.5, 'Carottes', '2023-09-27 18:21:00',1),
(2, 17.5, 'Tomates', '2020-08-14 13:23:00',1),
(3, 45.5, 'Pommes', '2020-10-02 15:38:00',2),
    (4, 4.5, '4 rue de la Paix'),
    (5, 5.5, '5 rue de la Paix'),
    (6, 6.5, '6 rue de la Paix');
