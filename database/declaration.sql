CREATE TABLE DECLARATION (
    no_declaration INTEGER PRIMARY KEY,
    date_declaration DATETIME NOT NULL,
    date_insp_vispre DATETIME NOT NULL,
    nbr_extermin INTEGER NOT NULL,
    date_debuttrait DATETIME NOT NULL,
    date_finittrait DATETIME NOT NULL,
    no_qr varchar(5) NOT NULL,
    nom_qr varchar(80) NOT NULL,
    nom_arrond varchar(80) NOT NULL,
    coord_x DECIMAL(6, 1) NOT NULL,
    coord_y DECIMAL(7, 1) NOT NULL,
    longitude DECIMAL(2, 6)NOT NULL,
    latitude DECIMAL(2, 6) NOT NULL
);

create table profil_user (
  id INTEGER PRIMARY KEY,
  nom NVARCHAR(300),
  email NVARCHAR(200),
  quartier NVARCHAR(300),
  salt varchar(60),
  hash varchar(130)
);