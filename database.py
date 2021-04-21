import sqlite3
from .declaration import Declaration


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