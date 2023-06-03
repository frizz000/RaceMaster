-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-06-03 13:00:53.38

-- tables
-- Table: Osoba
CREATE TABLE Osoba (
    id integer NOT NULL CONSTRAINT Osoba_pk PRIMARY KEY,
    imie varchar(20) NOT NULL,
    drugieImie varchar(20),
    nazwisko varchar(20) NOT NULL,
    dataUr date NOT NULL,
    nrTelefonu varchar(20) NOT NULL,
    daneOpiekuna varchar(40)
);

-- Table: Przejazd
CREATE TABLE Przejazd (
    id integer NOT NULL CONSTRAINT Przejazd_pk PRIMARY KEY,
    czas float NOT NULL,
    zawodnikId integer NOT NULL,
    notatka varchar2(100) NOT NULL,
    CONSTRAINT Przejazd_Zawodnik FOREIGN KEY (zawodnikId)
    REFERENCES Zawodnik (id)
);

-- Table: Zawodnik
CREATE TABLE Zawodnik (
    id integer NOT NULL CONSTRAINT Zawodnik_pk PRIMARY KEY,
    pojazd varchar(20) NOT NULL,
    Osoba_id integer NOT NULL,
    Zawody_id integer NOT NULL,
    CONSTRAINT Zawodnik_Osoba FOREIGN KEY (Osoba_id)
    REFERENCES Osoba (id),
    CONSTRAINT Zawodnik_Zawody FOREIGN KEY (Zawody_id)
    REFERENCES Zawody (id)
);

-- Table: Zawody
CREATE TABLE Zawody (
    id integer NOT NULL CONSTRAINT Zawody_pk PRIMARY KEY,
    nazwa varchar2(20) NOT NULL,
    typ varchar2(20) NOT NULL,
    data date NOT NULL
);

-- End of file.

