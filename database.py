import sqlite3
import uuid
import hashlib
from .declaration import Declaration

# Base de données
class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("database/declaration.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def insert_data(self, array):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.executemany(
            ("REPLACE INTO DECLARATION(no_declaration,date_declaration,date_insp_vispre,nbr_extermin,date_debuttrait,date_finittrait,no_qr,nom_qr,nom_arrond,coord_x,coord_y,longitude,latitude)" "values(?,?,?,?,?,?,?,?,?,?,?,?,?)"), (array))
        connection.commit()

    def get_nom_qr(self, decla):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("SELECT * FROM DECLARATION WHERE nom_qr LIKE ?"), ('%' + decla + '%',))
        exist = cursor.fetchall()
        return exist

    def get_nom_arrond(self, decla):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("SELECT * FROM DECLARATION WHERE nom_arrond LIKE ?"), ('%' + decla + '%',))
        exist = cursor.fetchall()
        return exist


    def get_decla(self,from_date,to_date):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT * FROM DECLARATION WHERE date_declaration BETWEEN ? and ?"), (from_date,to_date,))
        declas = cursor.fetchall()
        return (Declaration(decla[0],decla[1],decla[2],decla[3],decla[4],decla[5],decla[6],decla[7],decla[8],decla[9],decla[10],decla[11],decla[12]) for decla in declas)

    def get_list_quartier(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select distinct nom_qr from DECLARATION order by nom_qr")
        quartiers = cursor.fetchall()
        return [(qr[0]) for qr in quartiers]

    def get_profil(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("select email from profil_user "
                       "where email = ? ", (email,))
        email_user = cursor.fetchall()
        return [(email[0]) for email in email_user]

    def insert_profil(self, nom, email, listeqr, mdp):
        connection = self.get_connection()
        cursor = connection.cursor()
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()

        cursor.execute(("insert into profil_user(nom, email, quartier, salt, hash) "
                        "values(?,?,?,?,?)"),
                       (nom, email, listeqr,salt, hashed_password))
        connection.commit()