from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func
import folium

from .app import app, db
from .modeles.classes_generic import *
from .modeles.classes_relationships import *
from .constantes import PERPAGE, cartes, statics
from .constantes_query import last_nominations, last_artistes, last_galeries, last_themes, last_villes

# ----- ROUTES GÉNÉRALES ----- #
@app.route("/")
def accueil():
    """Route utilisée pour la page d'accueil
    :return: render_template permettant la visualisation de la page d'accueil
    """
    artistes = Artiste.query.order_by(Artiste.id.desc()).limit(5).all()
    return render_template("pages/accueil.html", artistes=artistes,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)

# IL FAUDRA LA SUPPRIMER CELLE LÀ
@app.route("/hi")
def hi():
    return render_template("pages/hi.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/about")
def about():
    return render_template("pages/about.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/recherche", methods=["GET", "POST"])
def recherche():
    """Route pour la recherche en plein texte

    :return:
    """
    # initialisation de la recherche: pagination et définition des variables pour stocker les résultats
    keyword = request.args.get("keyword", None)
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    results_nomination = []
    results_artiste = []
    results_galerie = []
    results_theme = []
    results_ville = []
    titre = f"Résultats pour la recherche : {keyword}"

    if keyword:
        # traduction de la requête pour pouvoir rechercher les nominé.e.s ou lauréat.e.s
        if keyword == "lauréat" \
            or keyword == "lauréate" \
            or keyword == "lauréat.e" \
            or keyword == "lauréats" \
            or keyword == "nominées" \
            or keyword == "lauréat.e.s":
            keyword = 1
        elif keyword == "nominé" \
            or keyword == "nominée" \
            or keyword == "nominé.e" \
            or keyword == "nominés" \
            or keyword == "nominées" \
            or keyword == "nominé.e.s":
            keyword = 0
        # requête sur toutes les tables
        results_nomination = Nomination.query.filter(Nomination.id.like(f"%{keyword}%"))
        results_nomination = results_nomination.with_entities(Nomination.laureat)
        results_artiste = Artiste.query.filter(db.or_(Artiste.nom.like(f"%{keyword}%"), Artiste.prenom.like(f"%{keyword}%")))
        results_artiste = results_artiste.with_entities(Artiste.full)
        results_galerie = Galerie.query.filter(Galerie.nom.like(f"%{keyword}%"))
        results_galerie = results_galerie.with_entities(Galerie.nom)
        results_ville = Ville.query.filter(Galerie.nom.like(f"%{keyword}%"))
        results_ville = results_ville.with_entities(Ville.full)
        results_theme = Theme.query.filter(Theme.nom.like(f"%{keyword}%"))
        results_theme = results_theme.with_entities(Theme.nom)

    results = results_nomination.union(results_artiste, results_galerie, results_theme, results_ville)
    print(results.paginate(page=page, per_page=PERPAGE))
    return render_template(
        "pages/recherche_results.html",
        results_nomination=results_nomination,
        results_artiste=results_artiste,
        results_galerie=results_galerie,
        results_theme=results_theme,
        results_ville=results_ville,
        titre=titre,
        keyword=keyword,
        last_nominations = last_nominations, last_artistes = last_artistes, last_galeries = last_galeries,
        last_themes = last_themes, last_villes = last_villes
    )



# ----- ROUTES ARTISTE ----- #
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
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    artistes = Artiste.query.join(Nomination, Artiste.id == Nomination.id_artiste)\
        .order_by(Artiste.id.desc()).paginate(page=page, per_page=PERPAGE)
    return render_template("pages/artiste_index.html", titre=titre, artistes=artistes,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


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
        return render_template("pages/artiste_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


# ----- ROUTES NOMINATION ----- #
@app.route("/nomination")
def nomination_index():
    """Fonction permettant d'afficher un index de toutes les nominations figurant dans la base de données
    avec une pagination. La pagination est faite en fonction de l'édition du prix : chaque page correspond
    à une année du prix Marcel Duchamp

    :return: renvoi vers le fichier html d'index des nominations
    :rtype: objet render_template
    """
    page = request.args.get("page", 1)
    titre = "Nominations"
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id)\
        .join(Theme, Nomination.id_theme == Theme.id)\
        .order_by(Nomination.id.desc()).paginate(page=page, per_page=PERPAGE)
    return render_template \
        ("pages/nomination_index.html", titre=titre, nominations=nominations,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/nomination/<int:id_nomination>")
def nomination_main():
    """page détaillée sur une nomination
    PEUT-ÊTRE QU'IL FAUDRA REMPLACER ÇA VERS UN RENVOI À ARTISTE_MAIN ?"""

@app.route("/nomination.add", methods=["GET", "POST"])
def nomination_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
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
            return render_template("pages/nomination_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
    else:
        return render_template("pages/nomination_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


# ----- ROUTES GALERIE ----- #
@app.route("/galerie")
def galerie_index():
    """Fonction permettant d'afficher un index de toutes les galeries figurant dans la base de données
    avec une pagination.

    :return: renvoi vers le fichier html d'index des galeries
    :rtype: objet render_template
    """
    page = request.args.get("page", 1)
    titre = "Galeries"
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    galeries = Galerie.query.order_by(Galerie.id.desc()).paginate(page=page, per_page=PERPAGE)
    return render_template("pages/galerie_index.html", titre=titre, galeries=galeries,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)

@app.route("/galerie/<int:id_galerie>")
def galerie_main():
    """fonction pour afficher la page principale d'une galerie
    ESSAYER D'INTÉGRER DE LA CARTOGRAPHIE DANS CETTE PAGE"""

@app.route("/galerie/add", methods=["POST", "GET"])
def galerie_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
    # si il.elle est connecté.e et si un formulaire est envoyé avec post
    if request.method == "POST":
        succes, donnees = Galerie.galerie_new(
            nom=request.form.get("nom", None)
        )
        if succes is True:
            flash("Vous avez rajouté une nouvelle galerie à la base de données", "success")
            return redirect("/artiste",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
        else:
            flash("L'ajout de données n'a pas pu être fait: " + " + ".join(donnees), "error")
            return render_template("pages/galerie_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
    else:
        return render_template("pages/galerie_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


# ----- ROUTES VILLE ----- #
@app.route("/ville")
def ville_index():
    """Fonction permettant d'afficher un index de toutes les galeries figurant dans la base de données
    avec une pagination.

    :return: renvoi vers le fichier html d'index des galeries
    :rtype: objet render_template
    """
    page = request.args.get("page", 1)
    titre = "Villes"
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    villes = Ville.query.order_by(Ville.id.asc()).paginate(page=page, per_page=PERPAGE)
    return render_template("pages/ville_index.html", titre=titre, villes=villes,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/ville/<int:id_ville>")
def ville_main(id_ville):
    """fonction pour la création de ville.
    essayer d'ajouter de la géolocalisation"""

    # jointures et génération de données pour les popups
    ville = Ville.query.get(id_ville)
    ville_artiste_naissance = Artiste.query.join(Ville, Artiste.id_ville_naissance == Ville.id)\
        .filter(Ville.id == id_ville).all()
    ville_artiste_residence = Artiste.query.join(Ville, Artiste.id_ville_residence == Ville.id)\
        .filter(Ville.id == id_ville).all()
    ville_galerie = RelationLocalisation.query.join(Ville, RelationLocalisation.id_ville == Ville.id)\
        .join(Galerie, RelationLocalisation.id_galerie == Galerie.id).filter(Ville.id == id_ville).all()

    # création du css et du texte d'un popup qui donnera des informations sur chaque ville
    css = """
        @font-face {
          font-family: 'Mels';
          src: url('static/fonts/Mels-Regular.otf'), url('static/fonts/Mels-Italic.otf') format('opentype');
          font-weight: normal;
          font-style: normal;
        }
        
        * {
          font-family: "Mels", "Helvetica Neue", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
          color: #bd148b;
          background-color: #ffb0ff;
        }
    """
    html = f"<head><meta charset='UTF-8'/><style type='text/css'>{css}</style><h2>" + ville.nom + "</h2>"
    if ville_artiste_naissance:
        html += "<p>Dans cette ville est né.e :</p><ul>"
        for artiste in ville_artiste_naissance:
            html += f"<li>{artiste.prenom} {artiste.nom}</li>"
        html += "</ul>"
    if ville_artiste_residence:
        html += "<p>Dans cette ville habite(nt) :</p><ul>"
        for artiste in ville_artiste_residence:
            html += f"<li>{artiste.prenom} {artiste.nom}</li>"
        html += "</ul>"
    if ville_galerie:
        html += "<p>Dans cette ville se trouve(nt) la/les galeries suivante(s) :</p><ul>"
        for rel in ville_galerie:
            html += f"<li>{rel.galerie.nom}</li>"
        html += "</ul>"

    # transformation du popup en élément iframe
    iframe = folium.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)

    # génération d'une carte intégrée à la page; la carte est sauvegardée dans un dossier et
    # appelée lorsque l'on va sur la page de la ville
    carte = folium.Map(location=[ville.latitude, ville.longitude], tiles='Stamen Toner')
    popups = folium.CircleMarker(
        location=[ville.latitude, ville.longitude],
        popup=popup,
        radius=1000,
        color="purple",
        fill_color="plum",
        fill_opacity=100
    ).add_to(carte)
    carte.save(f"{cartes}/ville{id_ville}.html")

    return render_template("pages/ville_main.html", ville=ville, carte=carte,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/ville/add", methods=["POST", "GET"])
def ville_ajout():
    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/login",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
    # si il.elle est connecté.e et si un formulaire est envoyé avec post
    if request.method == "POST":
        succes, donnees = Ville.ville_new(
            nom=request.form.get("nom", None),
            longitude=request.form.get("longitude", None)
        )
        if succes is True:
            flash("Vous avez rajouté une nouvelle ville à la base de données", "success")
            return redirect("/ville",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
        else:
            flash("L'ajout de données n'a pas pu être fait: " + " + ".join(donnees), "error")
            return render_template("pages/ville_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)
    else:
        return render_template("pages/ville_ajout.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


# ----- ROUTES THEME ----- #
@app.route("/theme")
def theme_index():
    """Fonction permettant d'afficher un index de tous les thèmes figurant dans la base de données
    avec une pagination.

    :return: renvoi vers le fichier html d'index des galeries
    :rtype: objet render_template
    """
    page = request.args.get("page", 1)
    titre = "Thèmes"
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    themes = Theme.query.order_by(Theme.id.desc()).paginate(page=page, per_page=PERPAGE)
    return render_template("pages/theme_index.html", titre=titre, themes=themes,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/theme/<int:id_theme>")
def theme_main():
    """fonction pour afficher la page principale d'un thème"""

@app.route("/theme/add", methods=["POST", "GET"])
def theme_add():
    """fonction de création d'un nouveau thème"""


# ----- ROUTES CARTES ----- #
@app.route("/carte/<int:id>")
def carte(id):
    return render_template(f"partials/maps/ville{id}.html")

"""
@app.route("/sidebar")
def sidebar():
    last_artistes = Artiste.query.order_by(Artiste.id.desc()).limit(5).all()
    last_nominations = artistes = Artiste.query.join(Nomination, Artiste.id == Nomination.id_artiste) \
        .order_by(Artiste.id.desc()).limit(5).all
    last_galeries = Galerie.query.order_by(Galerie.id.desc()).limit(5).all()
    last_villes = Ville.query.order_by(Ville.id.desc()).limit(5).all()
    last_themes = Theme.query.order_by(Theme.id.desc()).limit(5).all()
    return render_template("partials/sidebar.html", last_nominations=last_nominations, last_artistes=last_artistes,
                           last_galeries=last_galeries, last_villes=last_villes, last_themes=last_themes)
"""