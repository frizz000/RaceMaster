-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-06-06 15:16:14.031

-- tables
-- Table: Kategoria
CREATE TABLE Kategoria (
    id integer NOT NULL CONSTRAINT Kategoria_pk PRIMARY KEY,
    nazwa varchar(50) NOT NULL,
    rokUrodzeniaStart integer NOT NULL,
    rokUrodzeniaEnd integer NOT NULL
);

-- Table: Przejazd
CREATE TABLE Przejazd (
    id integer NOT NULL CONSTRAINT Przejazd_pk PRIMARY KEY,
    czasPrzejazdu double NOT NULL,
    notatka varchar(100),
    Zawodnik_id integer NOT NULL,
    CONSTRAINT Przejazd_Zawodnik FOREIGN KEY (Zawodnik_id)
    REFERENCES Zawodnik (id)
);

-- Table: Zawodnik
CREATE TABLE Zawodnik (
    id integer NOT NULL CONSTRAINT Zawodnik_pk PRIMARY KEY,
    imie varchar(50) NOT NULL,
    nazwisko varchar(50) NOT NULL,
    plec varchar(50) NOT NULL,
    dataUrodzenia date NOT NULL,
    nrTelefonu varchar(50) NOT NULL,
    daneOpiekuna varchar(100),
    pojazd varchar(50) NOT NULL,
    Kategoria_id integer,
    CONSTRAINT Zawodnik_Kategoria FOREIGN KEY (Kategoria_id)
    REFERENCES Kategoria (id)
);


INSERT INTO Kategoria (nazwa, rokUrodzeniaStart, rokUrodzeniaEnd) VALUES
    ('Dorośli', 1988, 2002),
    ('Młodzież', 2003, 2007),
    ('Dzieci', 2008, 2023);

INSERT INTO Zawodnik (imie, nazwisko, plec, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd, Kategoria_id) VALUES
    ('Jan', 'Kowalski', 'M', '1990-05-10', '123456789', 'Anna Kowalska', 'rower', 1),
    ('Anna', 'Nowak', 'K', '2005-07-15', '987654321', 'Jan Nowak', 'hulajnoga', 2),
    ('Adam', 'Wiśniewski', 'M', '2010-12-03', '456123789', 'Ewa Wiśniewska', 'rower', 3);

INSERT INTO Przejazd (czasPrzejazdu, notatka, Zawodnik_id) VALUES
    (15.6, 'Bardzo dobry czas!', 1),
    (18.3, 'Poprawa w stosunku do ostatniego przejazdu.', 2),
    (20.1, 'Pierwszy przejazd.', 3);

-- End of file.

