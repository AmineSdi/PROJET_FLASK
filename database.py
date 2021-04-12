import sqlite3


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

    def update_db(self,reader):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.executemany(
            ("REPLACE INTO DECLARATION(no_declaration,date_declaration,date_insp_vispre,nbr_extermin,date_debuttrait,date_finittrait,no_qr,nom_qr,nom_arrond,coord_x,coord_y,longitude,latitude)" "values(?,?,?,?,?,?,?,?,?,?,?,?,?)"), (reader))
        connection.commit()
