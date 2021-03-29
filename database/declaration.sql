CREATE TABLE DECLARATION (
    no_declaration integer PRIMARY KEY,
    date_insp_vispre DATETIME,
    nbr_extermin integer,
    date_debuttrait DATETIME,
    date_finittrait DATETIME,
    no_qr varchar(3),
    nom_qr varchar(50),
    nom_arrond varchar(60),
    coord_x DECIMAL(6, 1),
    coord_y DECIMAL(7, 1),
    longitude DECIMAL(2, 6),
    latitude DECIMAL(2, 6)
);