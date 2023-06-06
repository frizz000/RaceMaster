-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-06-06 11:49:45.577

-- tables
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
    dataUrodzenia date NOT NULL,
    nrTelefonu varchar(50) NOT NULL,
    daneOpiekuna varchar(100),
    pojazd varchar(50) NOT NULL
);

-- End of file.

