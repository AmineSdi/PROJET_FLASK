from flask import Flask, jsonify,redirect, render_template, request, url_for, g
import requests
import sqlite3
from .declaration import Declaration
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import re
import csv
from .database import Database
from datetime import datetime


app = Flask(__name__, static_url_path="", static_folder="static")
app.config['JSON_AS_ASCII'] = False

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

# Importer les données de la ville de montréal
def import_data():

    req = requests.get(
        "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv")

    url_content = req.content

    csv_file = open('declaration_punaises.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

#Mettre à jour les données dans la base de données
def data_handler():
    with app.app_context():
        print("On met à jour la base de donnée ...")
        import_data()
    
        with open('declaration_punaises.csv') as csvfile:

            reader = csv.reader(csvfile)     
            next(reader)
            get_db().insert_data(reader) 

        csvfile.close()
        print("Mise à jour complétée.")

# BACKGROUNDSCHEDULER: Enclencher la fonction data_handler tous les jours à minuit.
scheduler = BackgroundScheduler()
scheduler.add_job(func=data_handler, trigger="cron", hour='00',minute='00')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Fonction main (principale)

import_data()
data_handler()

def valider_iso(input):
    regex = re.match(
        "^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$", input)
    is_match = bool(regex)
    return is_match

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

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


@ app.route("/api/declarations", methods=["GET"])
def get_declas():

    from_date = request.args.get("du")
    print("\n--------------------\n")
    print(type(from_date))
    print(from_date)
    to_date = request.args.get("au")
    print(to_date)
    print("\n--------------------\n")
    

    valid_from = valider_iso(from_date)
    print("au: ",valid_from)
    valid_to = valider_iso(to_date)
    print("du:",valid_to)

    if valid_from == False or valid_to == False:
        return jsonify({'resultat':'Erreur: format ISO8601 non respecté'})

    elif valid_from == True and valid_to == True:

        declas = get_db().get_decla(from_date,to_date)

        if not declas or declas is None:
            return jsonify({'resultat':'Aucun résultat trouvé entre les deux dates spécifiées'})

        else :
            print("\n--------------------\n")
            print(declas)
            print("\n--------------------\n")
            return jsonify([decla.get_decla() for decla in declas])

@ app.route("/doc", methods=["GET"])
def afficher_raml():
    return render_template("doc.html")