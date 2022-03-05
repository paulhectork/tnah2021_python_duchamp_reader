from flask import render_template, url_for, request, flash, redirect, jsonify
from flask_login import current_user, login_user, logout_user

from .app import app
from .modeles.classes_generic import *
from .constantes import PERPAGE

@app.route("/")
def accueil():
    """Route utilisée pour la page d'accueil
    :return: render_template permettant la visualisation de la page d'accueil
    """
    artistes = Artiste.query.order_by(Artiste.id.desc()).limit(5).all()
    return render_template("pages/accueil.html", artistes=artistes)


# IL FAUDRA LA SUPPRIMER CELLE LÀ
@app.route("/hi")
def hi():
    return render_template("pages/hi.html")


@app.route("/about")
def about():
    return render_template("pages/about.html")


@app.route("/recherche", methods=["GET", "POST"])
def recherche():
    pass # RAJOUTER LA FONCTION PLUS TARD


@app.route("/artiste")
def artiste_index():
    """Fonction permettant d'afficher un index de tou.te.s les artistes figurant dans la base de données
    avec une pagination. La pagination est faite en fonction de l'édition du prix : chaque page correspond
    à une année du prix Marcel Duchamp

    :return: renvoi vers le fichier html d'index des artistes
    :rtype: objet render_template
    """
    page = request.args.get("page", 1)
    titre = "Artistes"

    # pagination
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    artistes = Artiste.query.order_by(Artiste.id.desc()).paginate(page=page, per_page=PERPAGE)

    # afficher dynamiquement une année par page de la requête
    nominations = Nomination.query.group_by(Nomination.annee).order_by(Nomination.annee)
    annees = []
    for nomination in nominations:
        annees.append(nomination.annee)

    return render_template("pages/artiste_index.html", titre=titre, artistes=artistes, annees=annees)


@app.route("/artiste/<int:id_artiste>")
def artiste_main():
    """page détaillée sur un.e artiste"""


@app.route("/artiste/add", methods=["GET", "POST"])
def artiste_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error") #syntaxe de flash: flash("message", "category"): "flash("To contribute, log in or sign in", "info")"
        return redirect("/login")
    # si il.elle est connecté.e et si un formulaire est envoyé avec POST
    if request.method == "POST":
        succes, donnees = Artiste.artiste_new(
            nom=request.form.get("nom", None),
            prenom=request.form.get("prenom", None),
            annee_naissance=request.form.get("annee_naissance", None),
            genre=request.form.get("genre", None),
            ville_naissance=request.form.get("ville_naissance", None),
            ville_residence=request.form.get("ville_residence", None)
        )
        if succes is True:
            flash("Vous avez ajouté un.e nouvel.le artiste à la base de données", "success")
            return redirect("/artiste") # url de redirection, on peut changer
        else:
            flash("Error: " + " + ".join(donnees), "error") # data c'est quoi ?? je l'ai trouvé dans le devoir StoneAdvisor
            return render_template("pages/artiste_ajout.html") # artiste_ajout : fichier html contenant le formulaire d'ajout d'artiste
    else:
        return render_template("pages/artiste_ajout.html")


@app.route("/nomination")
def nomination_index():
    page = request.args.get("page", 1)
    titre = "Nominations"

    # pagination
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id)\
        .order_by(Nomination.id.desc()).paginate(page=page, per_page=PERPAGE)

    # afficher dynamiquement une année par page de la requête
    nom_annees = Nomination.query.group_by(Nomination.annee).order_by(Nomination.annee)
    annees = []
    for nom_annee in nom_annees:
        annees.append(nom_annee.annee)
    return render_template\
        ("pages/nomination_index.html", titre=titre, nominations=nominations, annees=annees)


@app.route("/nomination/<int:id_nomination>")
def nomination_main():
    """page détaillée sur une nomination"""
    # PEUT-ÊTRE QU'IL FAUDRA REMPLACER ÇA VERS UN RENVOI À ARTISTE_MAIN ?

@app.route("/nomination.add", methods=["GET", "POST"])
def nomination_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login")
    # si il.elle est connecté.e et si un formulaire est envoyé avec post
    if request.method == "POST":
        succes, donnees = Nomination.nomination_new(
            annee=request.form.get("annee", None),
            laureat=request.form.get("laureat", None),
            nom_artiste=request.form.get("nom_artiste", None),
            prenom_artiste=request.form.get("prenom_artiste", None),
            theme=request.form.get("theme", None)
        )
        if succes is True:
            flash("Vous avez rajouté une nouvelle nomination au prix Marcel Duchamp dans la base", "success")
            return redirect("/nomination")
        else:
            flash("L'ajout de données n'a pas pu être fait: " + " + ".join(donnees), "error")
            return render_template("pages/nomination_ajout.html")
    else:
        return render_template("pages/nomination_ajout.html")

@app.route("/galerie")
@app.route("/galerie/<int:id>")
@app.route("/galerie/add", methods=["POST", "GET"])
def galerie_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login")
    # si il.elle est connecté.e et si un formulaire est envoyé avec post
    if request.method == "POST":
        succes, donnees = Galerie.galerie_new(
            nom=request.form.get("nom", None)
        )
        if succes is True:
            flash("Vous avez rajouté une nouvelle galerie à la base de données", "success")
            return redirect("/artiste")
        else:
            flash("L'ajout de données n'a pas pu être fait: " + " + ".join(donnees), "error")
            return render_template("pages/galerie_ajout.html")
    else:
        return render_template("pages/galerie_ajout.html")

@app.route("/ville")
@app.route("/ville/<int:id>")
@app.route("/ville/add", methods=["POST", "GET"])
def ville_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login")
    # si il.elle est connecté.e et si un formulaire est envoyé avec post
    if request.method == "POST":
        succes, donnees = Ville.ville_new(
            nom=request.form.get("nom", None),
            longitude=request.form.get("longitude", None)
        )
        if succes is True:
            flash("Vous avez rajouté une nouvelle ville à la base de données", "success")
            return redirect("/ville")
        else:
            flash("L'ajout de données n'a pas pu être fait: " + " + ".join(donnees), "error")
            return render_template("pages/ville_ajout.html")
    else:
        return render_template("pages/ville_ajout.html")

"""
@app.route("/theme")
@app.route("/theme/<int:id>")
@app.route("/theme/add", methods=["POST", "GET"])
# j'ai pas encore créé ma staticmethod de création pour Theme, donc j'attends pour faire la route
"""