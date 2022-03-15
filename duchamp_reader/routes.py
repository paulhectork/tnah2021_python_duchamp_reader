from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_user, logout_user
import folium

from .app import app, db
from .modeles.classes_generic import *
from .modeles.classes_relationships import *
from .constantes import PERPAGE, cartes, statics, css
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
    """Route pour faire une recherche rapide sur toutes les tables

    :return:
    """
    # initialisation de la recherche: pagination, définition du titre, initialisation des variables
    keyword = request.args.get("keyword", None)
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    results_artiste = []
    results_galerie = []
    results_theme = []
    results_ville = []
    results = None
    titre = f"Résultats pour la recherche : {keyword}"

    if keyword:
        # requête sur toutes les tables SAUF LA TABLE NOMINATION parce qu'il n'y a rien de bien intéressant
        results_artiste = Artiste.query.filter(db.or_(Artiste.nom.like(f"%{keyword}%"),
                                                      Artiste.prenom.like(f"%{keyword}%")))\
            .with_entities(Artiste.classname, Artiste.id, Artiste.full.label("data"))
        results_galerie = Galerie.query.filter(Galerie.nom.like(f"%{keyword}%"))\
            .with_entities(Galerie.classname, Galerie.id, Galerie.nom.label("data"))
        results_ville = Ville.query.filter(db.or_(Ville.nom.like(f"%{keyword}%"),
                                                      Ville.pays.like(f"%{keyword}%")))\
            .with_entities(Ville.classname, Ville.id, Ville.full.label("data"))
        results_theme = Theme.query.filter(Theme.nom.like(f"%{keyword}%"))\
            .with_entities(Theme.classname, Theme.id, Theme.nom.label("data"))

        results = results_artiste.union(results_galerie, results_ville, results_theme)\
            .order_by(Artiste.id.asc()).paginate(page=page, per_page=PERPAGE)

        # en SQL, UNION permet d'empiler des requêtes avec le même nombre de colonnes et les mêmes
        # noms de colonnes. c'est pour ça qu'on utilise ".with_entities()", pour sélectionner les colonnes
        # à conserver et ".label()" pour renommer les colonnes. la requête au dessus équivaut à:
        #   SELECT nomination.id, nomination.annee AS data, nomination.classname
	    #   FROM nomination
        #   UNION
        #   SELECT artiste.id, artiste.nom AS data, artiste.classname
	    #   FROM artiste

    return render_template(
        "pages/recherche_results.html", results=results, titre=titre, keyword=keyword,
        last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
        last_themes=last_themes, last_villes=last_villes
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
def artiste_main(id_artiste):
    """Page détaillée sur un.e artiste. Pour chaque artiste, des informations biographiques et
    sur leur nomination sont données. En plus, la page comporte une carte générée dynamiquement
    avec un point pour le lieu de naissance et un pour le lieu de résidence. Le zoom de la carte
    est généré dynamiquement, de même que la taille des popups.

    :return: objet render_template() renvoyant vers la page détaillée d'un.e artiste.
    :rtype: objet render_template()
    """
    # requêtes; la requête principale est sur Nomination: c'est la table qui fait la jointure entre toutes les données
    nomination = Nomination.query.filter(Nomination.id_artiste == id_artiste)\
        .join(Theme, Nomination.id_theme == Theme.id).first()
    represente = RelationRepresente.query.filter(RelationRepresente.id_artiste == id_artiste).all()
    nominations_all = Nomination.query.filter(Nomination.annee == nomination.annee).all()

    # génération dynamique des cartes
    # définition des coordonnées de la carte: zone sur laquelle centrer
    longitude = (nomination.artiste.ville_naissance.longitude + nomination.artiste.ville_residence.longitude) / 2
    latitude = (nomination.artiste.ville_naissance.latitude + nomination.artiste.ville_residence.latitude) / 2

    # définition des coordonnées de la carte: extrêmes nord-ouest et sud-est qui doivent être contenus dans chaque carte
    longlist = []
    latlist = []
    longlist.append(nomination.artiste.ville_naissance.longitude)
    longlist.append(nomination.artiste.ville_residence.longitude)
    latlist.append(nomination.artiste.ville_naissance.latitude)
    latlist.append(nomination.artiste.ville_residence.latitude)
    diflat = max(latlist) - min(latlist)
    diflong = max(longlist) - min(longlist)
    avglat = (max(latlist) + min(latlist)) / 2
    avglong = (max(longlist) + min(longlist)) / 2
    # définir les dimensions extrêmes de la carte
    if diflong > diflat:
        # si la largeur est plus grande que la longueur, longueur = 0.8 * largeur;
        # on centre la carte sur la longueur moyenne
        minlat = avglat - diflong * 0.8
        maxlat = avglat + diflong * 0.8
        sw = [minlat, min(longlist)]
        ne = [maxlat, max(longlist)]
    else:
        # si la longueur est plus grande que la largeur, largeur = 1.25 * longueur;
        # on centre la carte sur la largeur moyenne
        minlong = avglong - diflat * 1.25
        maxlong = avglong + diflat * 1.25
        sw = [min(latlist), minlong]
        ne = [max(latlist), maxlong]

    # définition de la taille des marqueurs, qui varie selon leur distance sur la carte
    if diflat > 50 or diflong > 50:
        radius = 300000
    elif diflat > 30 or diflong > 30:
        radius = 200000
    elif diflat > 5 or diflong > 5:
        radius = 50000
    elif diflat > 1 or diflong > 1:
        radius = 10000
    else:
        radius = 2000

    # création du texte d'un popup qui donnera des informations sur chaque ville
    html_residence = f"<html> \
                        <head><meta charset='UTF-8'/><style type='text/css'>{css}</style></head>\
                        <body> \
                            <p style='position:absolute; top:50%; left:50%; \
                                -ms-transform:translate(-50%, -50%); \
                                transform: translate(-50%, -50%); \
                                text-align: center;'>\
                                Ville de résidence : {nomination.artiste.ville_residence.nom}\
                            </p></body>\
                     </html>"
    html_naissance = f"<html> \
                        <head><meta charset='UTF-8'/><style type='text/css'>{css}</style></head>\
                        <body> \
                            <p style='position:absolute; top:50%; left:50%; \
                                -ms-transform:translate(-50%, -50%); \
                                transform: translate(-50%, -50%); \
                                text-align: center;'>\
                                Ville de naissance : {nomination.artiste.ville_naissance.nom} \
                            </p></body>\
                     </html>"
    iframe_residence = folium.element.IFrame(html=html_residence, width="300px", height="100px")
    iframe_naissance = folium.element.IFrame(html=html_naissance, width="300px", height="100px")
    popup_residence = folium.Popup(iframe_residence)
    popup_naissance = folium.Popup(iframe_naissance)

    # génération d'une carte intégrée à la page; la carte est sauvegardée dans un dossier et
    # appelée lorsque l'on va sur la page de l'artiste ; la taille des popups dépend de la distance entre eux
    carte = folium.Map(location=[latitude, longitude], tiles="Stamen Toner")
    if diflat > 1 or diflong > 1:
        carte.fit_bounds([sw, ne])
    popups_residence = folium.CircleMarker(
        location=[nomination.artiste.ville_residence.latitude, nomination.artiste.ville_residence.longitude],
        popup=popup_residence,
        radius=radius,
        color="purple",
        fill_color="plum",
        fill_opacity=0.6
    ).add_to(carte)
    popups_naissance = folium.CircleMarker(
        location=[nomination.artiste.ville_naissance.latitude, nomination.artiste.ville_naissance.longitude],
        popup=popup_naissance,
        radius=radius,
        color="purple",
        fill_color="plum",
        fill_opacity=0.6
    ).add_to(carte)
    carte.save(f"{cartes}/artiste{id_artiste}.html")

    # return
    return render_template("pages/artiste_main.html", nomination=nomination,
                           represente=represente, nominations_all=nominations_all, carte=carte,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


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
# il n'y a pas de route "nomination_main()" puisque  la page principale d'une nomination est la même
# que la page d'un.e artiste
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
    return render_template("pages/nomination_index.html", titre=titre, nominations=nominations,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


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
def galerie_main(id_galerie):
    """Page détaillée sur une galerie. Pour chaque galerie est donnée la liste des artistes représenté.e.s,
    et des villes où elle se trouve, ainsi qu'un lien vers le site web de la galerie. En plus, la page comporte
    une carte générée dynamiquement avec un point par ville où se trouve la galerie. Le zoom de la carte
    est généré dynamiquement, de même que la taille des popups.

    :return: objet render_template() renvoyant vers la page détaillée d'une galerie.
    :rtype: objet render_template()
    """
    # requêtes
    galerie = Galerie.query.filter(Galerie.id == id_galerie).first()
    print(galerie.nom)
    for r in galerie.represent:
        print(r.artiste.full)
    for r in galerie.localisation:
        print(r.ville.nom)

    # génération dynamique des cartes
    # définition des coordonnées de la carte: zone sur laquelle centrer
    nboucles = 0  # nombre de boucles, pour calculer la longitude et latitude moyenne
    longitude = 0  # longitude moyenne des différents points sur la carte
    latitude = 0  # latitude moyenne des différents points sur la carte
    longlist = []  # liste des longitudes des différents points sur la carte
    latlist = []  # liste des latitudes des différents points sur la carte
    for r in galerie.localisation:
        nboucles += 1
        longitude += r.ville.longitude
        latitude += r.ville.latitude
        longlist.append(r.ville.longitude)
        latlist.append(r.ville.latitude)
    longitude = longitude / nboucles
    latitude = latitude / nboucles
    diflat = max(latlist) - min(latlist)
    diflong = max(longlist) - min(longlist)
    avglat = (max(latlist) + min(latlist)) / 2
    avglong = (max(longlist) + min(longlist)) / 2

    # définir les dimensions extrêmes de la carte
    if diflong > diflat:
        # si la largeur est plus grande que la longueur, longueur = 0.8 * largeur;
        # on centre la carte sur la longueur moyenne
        minlat = avglat - diflong * 0.8
        maxlat = avglat + diflong * 0.8
        sw = [minlat, min(longlist)]
        ne = [maxlat, max(longlist)]
    else:
        # si la longueur est plus grande que la largeur, largeur = 1.25 * longueur;
        # on centre la carte sur la largeur moyenne
        minlong = avglong - diflat * 1.25
        maxlong = avglong + diflat * 1.25
        sw = [min(latlist), minlong]
        ne = [max(latlist), maxlong]

    # définition de la taille des marqueurs, qui varie selon leur distance sur la carte
    if diflat > 50 or diflong > 50:
        radius = 300000
    elif diflat > 30 or diflong > 30:
        radius = 200000
    elif diflat > 5 or diflong > 5:
        radius = 50000
    elif diflat > 1 or diflong > 1:
        radius = 10000
    else:
        radius = 2000

    # génération de la carte intégrée à la page; la carte est sauvegardée dans un dossier et
    # appelée lorsque l'on va sur la page de l'artiste
    carte = folium.Map(location=[latitude, longitude], tiles="Stamen Toner")
    if diflat > 1 or diflong > 1:
        carte.fit_bounds([sw, ne])

    # génération des popups à ajouter à la carte: 1 popup / ville où est située une galerie;
    # la taille des popups dépend de la distance entre eux sur la carte
    for r in galerie.localisation:
        html = f"<html> \
                    <head><meta charset='UTF-8'/><style type='text/css'>{css}</style></head>\
                        <body> \
                            <p style='position:absolute; top:50%; left:50%; \
                                -ms-transform:translate(-50%, -50%); \
                                transform: translate(-50%, -50%); \
                                text-align: center;'>\
                                La galerie {galerie.nom} se trouve à : {r.ville.nom}\
                            </p></body>\
                </html>"
        iframe = folium.element.IFrame(html=html, width="300px", height="100px")
        popup_galerie = folium.Popup(iframe)
        popups_galerie = folium.CircleMarker(
            location=[r.ville.latitude, r.ville.longitude],
            popup=popup_galerie,
            radius=radius,
            color="purple",
            fill_color="plum",
            fill_opacity=0.6
        ).add_to(carte)

    # sauvegarder la carte
    carte.save(f"{cartes}/galerie{id_galerie}.html")

    # return
    return render_template("pages/galerie_main.html", galerie=galerie, carte=carte,
                           last_nominations=last_nominations, last_artistes=last_artistes,
                           last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


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
    """Fonction permettant d'afficher les détails sur une ville, ainsi qu'une carte avec un
    "popup" qui liste toutes les données liées à la ville.

    :return: objet render_template renvoyant à la page html "ville_main.html"
    :rtype: render_template object
    """
    # jointures et génération de données pour les popups
    """ville_artiste_naissance = Artiste.query.join(Ville, Artiste.id_ville_naissance == Ville.id)\
        .filter(Ville.id == id_ville).all()
    ville_artiste_residence = Artiste.query.join(Ville, Artiste.id_ville_residence == Ville.id)\
        .filter(Ville.id == id_ville).all()"""
    ville_artiste_naissance = Artiste.query.filter(Artiste.id_ville_naissance == id_ville).all()
    ville_artiste_residence = Artiste.query.filter(Artiste.id_ville_residence == id_ville).all()
    ville_galerie = RelationLocalisation.query.filter(RelationLocalisation.id_ville == id_ville).all()
    if ville_artiste_naissance:
        ville = ville_artiste_naissance[0].ville_naissance
    elif ville_artiste_residence:
        ville = ville_artiste_residence[0].ville_residence
    else:
        ville = ville_galerie[0].ville

    # création du texte d'un popup qui donnera des informations sur chaque ville
    html = f"<head><meta charset='UTF-8'/><style type='text/css'>{css}</style></meta></head><h2>{ville.nom}</h2>"
    if ville_artiste_naissance:
        html += "<p>Dans cette ville est né.e :</p><ul>"
        for artiste in ville_artiste_naissance:
            html += f"<li>{artiste.full}</li>"
        html += "</ul>"
    if ville_artiste_residence:
        html += "<p>Dans cette ville habite(nt) :</p><ul>"
        for artiste in ville_artiste_residence:
            html += f"<li>{artiste.full}</li>"
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
def theme_main(id_theme):
    """fonction pour afficher la page principale d'un thème"""
    theme = Theme.query.filter(Theme.id == id_theme).first()
    return render_template("pages/theme_main.html", theme=theme,
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/theme/add", methods=["POST", "GET"])
def theme_add():
    """fonction de création d'un nouveau thème"""


# ----- ROUTES CARTES ----- #
@app.route("/carte_ville/<int:id>")
def carte_ville(id):
    return render_template(f"partials/maps/ville{id}.html")


@app.route("/carte_artiste/<int:id>")
def carte_artiste(id):
    return render_template(f"partials/maps/artiste{id}.html")


@app.route("/carte_galerie/<int:id>")
def carte_galerie(id):
    return render_template(f"partials/maps/galerie{id}.html")


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