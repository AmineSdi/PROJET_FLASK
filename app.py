from flask import Flask, redirect, render_template, request, url_for, g
# import requests
import sqlite3
import re
import csv
from .database import Database
from datetime import datetime


app = Flask(__name__, static_url_path="", static_folder="static")

## Connection avec la base de données ##


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


#############################################
"""
# Script pour télécharger le fichier CSV


def download_csv(str):

    req = requests.get(str)

    url_content = req.content

    csv_file = open('declaration_punaises.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

# Fonction main (principale)


url_decl = "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv"

download_csv(url_decl)

with app.app_context():

    a_file = open("declaration_punaises.csv")

    rows = csv.reader(a_file)
    next(rows)
    get_db().insert_data(rows)
    a_file.close()
"""


@app.route("/", methods=["POST", "GET"])
def accueil():
    return render_template("index.html")


@ app.route("/resultats", methods=["GET"])
def test():

    if request.method == "GET":

        value = request.args.get('decla')
        print(value)

        if value == "" or value is None:
            return redirect(url_for("accueil"))

        array_qr = get_db().get_nom_qr(value)
        array_arrond = get_db().get_nom_arrond(value)

        if not array_qr and not array_arrond:
            return render_template("declaration.html")
        if array_qr:
            print("\n Déclaration selon le quartier :", array_qr, "\n")
            return render_template("declaration.html", result=array_qr, value=value)
        if array_arrond:
            print("\n Déclaration selon l'arrondissement :",
                  array_arrond, "\n")
            return render_template("declaration.html", result=array_arrond, value=value)
