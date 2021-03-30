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
        cursor.execute(
            ("INSERT INTO DECLARATION(no_declaration,date_declaration,date_insp_vispre,nbr_extermin,date_debuttrait,date_finittrait,no_qr,nom_qr,nom_arrond,coord_x,coord_y,longitude,latitude)" "values(?,?,?,?,?,?,?,?,?,?,?,?,?)"), (
                array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7], array[8], array[9], array[10], array[11], array[12]))
        connection.commit()
