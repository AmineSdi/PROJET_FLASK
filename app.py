from flask import Flask, redirect, render_template, request, url_for, g
import requests
import sqlite3
import re
from .database import Database
from datetime import datetime


app = Flask(__name__, static_url_path="", static_folder="static")


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


url_decl = "https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv"


def download_csv():

    req = requests.get(url_decl)

    url_content = req.content
    csv_file = open('declaration_punaises.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()


download_csv()


@ app.route("/<matricule>/<date_du_jour>", methods=["GET", "POST"])
def addTime(matricule, date_du_jour):

    exist = get_db().get_donnees(matricule, date_du_jour)
    print("\n -Donnees exist : ", exist)

    if request.method == "GET":
        print("GET")
        return render_template("temps.html", exist=exist, matricule=matricule, date_du_jour=date_du_jour)

    if request.method == "POST":

        code_p = request.form["codep"]
        duree = request.form["duree"]

        print("\n -Code de projet: ", code_p)
        print("\n -Durée: ", duree)

        if code_p == "" or code_p is None:
            print("code p vide")
            return render_template("temps.html", exist=exist, matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_code="Le code de projet est obligatoire.")

        if duree == "" or duree is None:
            print("duree vide")
            return render_template("temps.html", exist=exist, matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_duree="la durée est obligatoire.")

        if duree.isdigit() == False:
            print("duree mauvais type")
            return render_template("temps.html", exist=exist, matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_duree_type="La durée indiquée est erronée.")

        else:
            if not exist or any(code_p in t for t in exist) == False:

                get_db().insert_data(matricule, code_p, date_du_jour, duree)

            elif exist or any(code_p in t for t in exist) == True:

                duree_codep = get_db().get_duree(code_p)
                new_duree = int(duree) + duree_codep[0]
                id_ = get_db().get_id(code_p)

                get_db().update_duree(new_duree, date_du_jour, id_[0])

            exist = get_db().get_donnees(matricule, date_du_jour)
            print("Donnée existantes après", exist)
            return render_template("temps.html", exist=exist, date_du_jour=date_du_jour, matricule=matricule)


@ app.route("/<matricule>/<date_du_jour>/modifier/<id>", methods=["GET", "POST"])
def modify(matricule, date_du_jour, id):
    if request.method == "GET":
        print("GET_MODIFY")
        return render_template("modification.html", matricule=matricule, date_du_jour=date_du_jour, id=id)

    if request.method == "POST":

        code_p = request.form["codep"]
        duree = request.form["duree"]

        print(code_p)
        print(duree)

        if code_p == "" or code_p is None:
            print("code p vide")
            return render_template("modification.html", matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_code="Le code de projet est obligatoire.", id=id)

        if duree == "" or duree is None:
            print("duree vide_MODIFYYY")
            return render_template("modification.html", matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_duree="la durée est obligatoire.", id=id)

        if duree.isdigit() == False:
            print("duree mauvais type")
            return render_template("modification.html", matricule=matricule, date_du_jour=date_du_jour, duree=duree, code_p=code_p, msg_duree_type="La durée indiquée est erronée.", id=id)

        else:
            print("GOOD_MODIFY")
            get_db().update_codep(code_p, date_du_jour, id)
            get_db().update_duree(duree, date_du_jour, id)

            return redirect(url_for("addTime", matricule=matricule, date_du_jour=date_du_jour))


def validerMat(input):
    regex = re.match("[A-Z]{3}-\d{2}", input)
    is_match = bool(regex)
    return is_match


@ app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@ app.route("/", methods=["GET", "POST"])
def accueil():

    if request.method == "GET":

        return render_template("index.html")

    if request.method == "POST":

        matricule = request.form["matricule"]
        print(matricule)

        mat_valide = validerMat(matricule)

        print(mat_valide)

        if matricule == "":

            return render_template("index.html", error="Le matricule est obligatoire")

        elif mat_valide == False:

            return render_template("index.html", error_format="Le numéro du matricule doit être conforme au format spécifié")

        else:
            date = datetime.now()
            date_str = date.strftime("%Y-%m-%d")
            return redirect(url_for("addTime", matricule=matricule, date_du_jour=date_str))


if __name__ == "__main__":
    app.run(debug=True)
