-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-06-03 11:55:10.064

-- tables
-- Table: Osoba
CREATE TABLE Osoba (
    id integer  NOT NULL,
    imie varchar2(20)  NOT NULL,
    drugieImie varchar2(20)  NULL,
    nazwisko varchar2(20)  NOT NULL,
    dataUr date  NOT NULL,
    nrTelefonu varchar2(12)  NOT NULL,
    daneOpiekuna varchar2(40)  NULL,
    CONSTRAINT Osoba_pk PRIMARY KEY (id)
) ;

-- Table: Przejazd
CREATE TABLE Przejazd (
    id integer  NOT NULL,
    Czas timestamp  NOT NULL,
    Zawodnik_id integer  NOT NULL,
    notatka varchar2(100)  NOT NULL,
    CONSTRAINT Przejazd_pk PRIMARY KEY (id)
) ;

-- Table: Zawodnik
CREATE TABLE Zawodnik (
    id integer  NOT NULL,
    Pojazd varchar2(20)  NOT NULL,
    Osoba_id integer  NOT NULL,
    Zawody_id integer  NOT NULL,
    CONSTRAINT Zawodnik_pk PRIMARY KEY (id)
) ;

-- Table: Zawody
CREATE TABLE Zawody (
    id integer  NOT NULL,
    nazwa varchar2(20)  NOT NULL,
    typ varchar2(20)  NOT NULL,
    data date  NOT NULL,
    CONSTRAINT Zawody_pk PRIMARY KEY (id)
) ;

-- foreign keys
-- Reference: Przejazd_Zawodnik (table: Przejazd)
ALTER TABLE Przejazd ADD CONSTRAINT Przejazd_Zawodnik
    FOREIGN KEY (Zawodnik_id)
    REFERENCES Zawodnik (id);

-- Reference: Zawodnik_Osoba (table: Zawodnik)
ALTER TABLE Zawodnik ADD CONSTRAINT Zawodnik_Osoba
    FOREIGN KEY (Osoba_id)
    REFERENCES Osoba (id);

-- Reference: Zawodnik_Zawody (table: Zawodnik)
ALTER TABLE Zawodnik ADD CONSTRAINT Zawodnik_Zawody
    FOREIGN KEY (Zawody_id)
    REFERENCES Zawody (id);

-- End of file.

