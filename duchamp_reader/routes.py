from flask import render_template, request, flash, redirect, send_file, url_for
from flask_login import current_user, login_user, logout_user
from urllib.parse import quote_plus, unquote_plus
import folium
import json
import os

from .app import app, db
from .modeles.classes_generic import *
from .modeles.classes_relationships import *
from .modeles.classes_users import *
from .utils.constantes import PERPAGE, cartes, statics, css, uploads
from .utils.constantes_query import last_nominations, last_artistes, last_galeries, last_themes, last_villes
from .utils.duchamp_sparqler import duchamp_sparqler
from .utils.wikimaker import wikimaker
from .utils.mapdimensions import mapdim


# gesion des flashes d'erreurs:
# les messages d'erreurs sont renvoyés à l'utilisateurice via jinja à l'aide de règles contenues dans le conteneur
# si il y a potentiellement plusieurs erreurs, les stocker dans une liste "erreurs". retyper cette liste en str et
# faire un join avec '~' pour permettre à Jinja d'afficher les erreurs dans un '<ul>' (oui c'est compliqué)
# et passer la variable "erreurs" au render_template
# sinon (un seul message d'erreur), flash directement le message d'erreur sans le stocker dans une variable


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


@app.route("/about")
def about():
    return render_template("pages/about.html",
                           last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                           last_themes=last_themes, last_villes=last_villes)


@app.route("/recherche", methods=["GET", "POST"])
def recherche():
    """Route pour faire une recherche rapide sur toutes les tables.

    :return: objet render_template avec la liste de tous les résultats et une pagination. Pour chaque
    résultat, un renvoi vers la page détaillée de ce résultat est possible.
    :rtype: objet render_template
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
    titre = f"résultats pour la recherche : {keyword}"

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

    # return
    return render_template(
        "pages/recherche_results.html", results=results, titre=titre, keyword=keyword,
        last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
        last_themes=last_themes, last_villes=last_villes)


# ----- ROUTES USER ----- #
@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """Route pour se créer un compte sur le site web. Si tout va bien, un message de tout va bien
    s'affiche. Sinon, un message d'erreur indique les erreurs.
    :return: Si il n'y a pas d'erreurs dans la création du compte, redirection vers la page
             d'accueil avec un message de succès. Sinon, render_template de la page d'inscription
             avec un message d'erreur.
    """

    # si le formulaire d'inscription est envoyé, créer un nv compte d'utilisateur.ice
    if request.method == "POST":
        mdp = request.form.get("mdp", None)
        mdpcheck = request.form.get("mdpcheck", None)

        # si la vérification du mot de passe échoue, ne pas ajouter l'utilisateur.ice
        if mdp != mdpcheck:
            erreurs = "Erreur de vérification de votre mot de passe"
            flash(erreurs, "error")
            return render_template("pages/inscription.html", erreurs=erreurs,
                                   last_nominations=last_nominations, last_artistes=last_artistes,
                                   last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)
        else:
            statut, donnees = User.usr_new(
                nom=request.form.get("nom", None),
                login=request.form.get("login", None),
                email=request.form.get("email", None),
                mdp=request.form.get("mdp", None)
            )
            if statut is True:
                flash("Compte créé. Vous pouvez à présent vous connecter", "success")
                return redirect("/")
            else:
                # afficher un message d'erreur sur la page
                erreurs = "~".join(str(d) for d in donnees)
                flash(str(erreurs), "error")
                return render_template("pages/inscription.html", erreurs=erreurs,
                                       last_nominations=last_nominations, last_artistes=last_artistes,
                                       last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)
    else:
        return render_template("pages/inscription.html",
                               last_nominations=last_nominations, last_artistes=last_artistes,
                               last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """Route pour se connecter au site web.Si tout va bien, un message de tout va bien s'affiche.
    Sinon, un message d'erreur indique les erreurs.
    :return: Si l'utilisateurice est déjà connecté.e, render_template vers la page de connexion
             avec un message indiquant qu'iel est déjà connecté.e. Si iel se connecte avec les bons
             identifiants, redirection vers la page d'acceuil avec un message de succès. Si iel se
             connecte avec les mauvais identifiants, render_template vers la page de connexion avec un
             message d'erreur.
    """
    # si l'utilisateurice est déjà conecté.e
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté.e. Veuillez vous déconnecter pour changer de compte.", "success")
        return render_template("pages/connexion.html",
                               last_nominations=last_nominations, last_artistes=last_artistes,
                               last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)

    # si l'utilisateurice envoie un formulaire de connexion
    if request.method == "POST":
        user = User.usr_connexion(
            login=request.form.get("login", None),
            mdp=request.form.get("mdp", None)
        )
        # si les identifiants sont corrects, connecter l'utilisateurice
        if user:
            flash("Connexion effectuée", "success")
            login_user(user)
            return redirect("/")
        else:
            flash("Login ou mot de passe incorrects", "error")
            return render_template("pages/connexion.html",
                                   last_nominations=last_nominations, last_artistes=last_artistes,
                                   last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)

    return render_template("pages/connexion.html",
                           last_nominations=last_nominations, last_artistes=last_artistes,
                           last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """Fonction pour déconnecter un.e utilisateurice.

    :return: déconnexion et redirection vers la page d'accueil
    """
    if current_user.is_authenticated is True:
        logout_user()
        flash("Vous êtes déconnecté.e", "success")
        return redirect("/")


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
    titre = "index des artistes"
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
    sur leur nomination sont données. La page est enrichie de texte issu de la page wikipedia de l'artiste
    (si elle existe). Si la page wikipedia n'existe pas, des renvois vers 4 pages wikipedia sont proposés
    au hasard (il y a tout un système de try...except bien complexe). Enfin, cette fonction génère
    dynamiquement une carte intégrée à la page. La carte comporte avec un point pour le lieu de
    naissance et un pour le lieu de résidence. Le zoom de la carte est généré dynamiquement,
    de même que la taille des popups.

    :return: objet render_template() renvoyant vers la page détaillée d'un.e artiste.
    :rtype: objet render_template()
    """
    # requêtes; la requête principale est sur Nomination: c'est la table qui fait la jointure entre toutes les données
    nomination = Nomination.query.filter(Nomination.id_artiste == id_artiste)\
        .join(Theme, Nomination.id_theme == Theme.id).first()
    represente = RelationRepresente.query.filter(RelationRepresente.id_artiste == id_artiste).all()
    nominations_all = Nomination.query.filter(Nomination.annee == nomination.annee).all()

    # enrichissement de la page avec wikipedia
    code, summary, bio, formation, carriere, travail, oeuvre, url, wikidict = \
        wikimaker(full=nomination.artiste.full, nom=nomination.artiste.nom)

    # génération dynamique des cartes, si il y a des données géolocalisées à afficher
    # définition des coordonnées de la carte: zone sur laquelle centrer, coordonnées de la carte, taille du popup
    if nomination.artiste.ville_naissance and nomination.artiste.ville_residence:
        longitude = (nomination.artiste.ville_naissance.longitude + nomination.artiste.ville_residence.longitude) / 2
        latitude = (nomination.artiste.ville_naissance.latitude + nomination.artiste.ville_residence.latitude) / 2
        longlist = []
        latlist = []
        longlist.append(nomination.artiste.ville_naissance.longitude)
        longlist.append(nomination.artiste.ville_residence.longitude)
        latlist.append(nomination.artiste.ville_naissance.latitude)
        latlist.append(nomination.artiste.ville_residence.latitude)
        sw, ne, radius, diflat, diflong = mapdim(longlist=longlist, latlist=latlist)

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
    else:
        carte = ""

    # return
    return render_template("pages/artiste_main.html", nomination=nomination, travail=travail,
                           oeuvre=oeuvre, code=code, summary=summary, bio=bio, formation=formation,
                           carriere=carriere, url=url, wikidict=wikidict, represente=represente,
                           nominations_all=nominations_all, carte=carte, last_nominations=last_nominations,
                           last_artistes=last_artistes, last_galeries=last_galeries, last_themes=last_themes,
                           last_villes=last_villes)


@app.route("/artiste/add", methods=["GET", "POST"])
def artiste_add():
    """Page servant à ajouter un.e nouvel.le artiste à la base de données. Si les villes de naissance
    et de résidence n'existent pas, elles sont ajoutées à la table "Ville" à cette occasion. Si tout va
    bien, un message de tout va bien s'affiche. Sinon, un message d'erreur indique les erreurs.

    :return: redirect vers la page de connexion l'utilisateur.ice n'est pas connecté.e; si il y a une
    erreur, render_template vers la page "artiste/add" avec les messages d'erreurs; si tout se passe bien,
    render_template vers la page "artiste/add" avec un message indiquant que la transaction s'est bien déroulée.
    """
    # les requêtes constantes sont relancées pour éviter une SQLAlchemy ProgrammingError
    last_artistes = Artiste.query.order_by(Artiste.id.desc()).limit(3).all()
    last_nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id) \
        .order_by(Nomination.id.desc()).limit(3).all()
    last_galeries = Galerie.query.order_by(Galerie.id.desc()).limit(3).all()
    last_villes = Ville.query.order_by(Ville.id.desc()).limit(3).all()
    last_themes = Theme.query.order_by(Theme.id.desc()).limit(3).all()

    # si l'utilisateur.ice n'est pas connecté.e
    if current_user.is_authenticated is False:
        flash("Veuillez vous connecter pour rajouter des données", "error")
        return redirect("/connexion")

    # si iel est connecté.e et si un formulaire est envoyé avec POST
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
            flash("Vous avez ajouté un.e nouvel.le artiste à la base de données.", "success")
            return redirect("/artiste/add")
        else:
            # afficher un message d'erreur sur la page
            erreurs = "~".join(str(d) for d in donnees)
            flash(erreurs, "error")
            return render_template("pages/artiste_add.html", erreurs=erreurs,
                                   last_nominations=last_nominations, last_artistes=last_artistes,
                                   last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)

    # return
    return render_template("pages/artiste_add.html",
                           last_nominations=last_nominations, last_artistes=last_artistes,
                           last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


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


@app.route("/nomination/add", methods=["GET", "POST"])
def nomination_add():
    # les requêtes constantes sont relancées pour éviter une SQLAlchemy ProgrammingError
    last_artistes = Artiste.query.order_by(Artiste.id.desc()).limit(3).all()
    last_nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id) \
        .order_by(Nomination.id.desc()).limit(3).all()
    last_galeries = Galerie.query.order_by(Galerie.id.desc()).limit(3).all()
    last_villes = Ville.query.order_by(Ville.id.desc()).limit(3).all()
    last_themes = Theme.query.order_by(Theme.id.desc()).limit(3).all()

    # si l'utilisateur.ice n'est pas connecté.e, le/la rediriger vers la page d'accueil
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
            # afficher un message d'erreur sur la page
            erreurs = "~".join(str(d) for d in donnees)
            print(erreurs)
            flash(erreurs, "error")
            return render_template("pages/nomination_add.html",
                                   last_nominations=last_nominations, last_artistes=last_artistes, last_galeries=last_galeries,
                                   last_themes=last_themes, last_villes=last_villes)
    else:
        return render_template("pages/nomination_add.html",
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
    titre = "index des galeries"
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
    # définition des coordonnées de la carte: zone sur laquelle centrée, bordures, dimension des popups
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
    sw, ne, radius, diflat, diflong = mapdim(longlist=longlist, latlist=latlist)

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
    titre = "index des villes"
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
    titre = "index des thèmes"
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


# ----- ROUTES SPARQL ----- #
@app.route("/duchamp_sparqler", methods=["POST", "GET"])
def sparql():
    # ne requêter que les artistes ayant un ID wikidata
    artistes = Artiste.query.filter(Artiste.id_wikidata != "").order_by(Artiste.id).all()
    erreurs = []

    # si un formulaire est envoyé avec post, récupérer les données
    if request.method == "POST":
        id_wikidata = request.form.get("id_wikidata")  # le seul des "input" dont la "value" importe
        url = request.form.get("url")
        collection = request.form.get("collection")
        img = request.form.get("img")
        id_isni = request.form.get("id_isni")
        id_viaf = request.form.get("id_viaf")
        id_bnf = request.form.get("id_bnf")
        id_congress = request.form.get("id_congress")
        id_artsy = request.form.get("id_artsy")
        export = request.form.get("export")
        # s'assurer que le formulaire comporte des données
        if id_wikidata == "None":
            erreurs.append("Veuillez indiquer un artiste à requêter.")
        if export == "None":
            erreurs.append("Veuillez sélectionner un format pour l'export.")
        if not url \
                and not collection \
                and not img \
                and not id_isni \
                and not id_viaf \
                and not id_bnf \
                and not id_congress \
                and not id_artsy:
            erreurs.append("Veuillez cocher au moins une des cases pour lancer une requête.")

        # si les données ont été fournies, activer la fonction duchamp_sparqler pour lancer la requête
        if len(erreurs) == 0:
            # stocker le nom de la personne recherchée pour générer les noms de fichiers
            artiste = Artiste.query.filter(Artiste.id_wikidata == id_wikidata).first()
            nom = artiste.nom
            outname, queryname, err, datadict = duchamp_sparqler(nom=nom, id_wikidata=id_wikidata, url=url,
                                                                 collection=collection, img=img, id_isni=id_isni,
                                                                 id_viaf=id_viaf, id_bnf=id_bnf,
                                                                 id_congress=id_congress, id_artsy=id_artsy,
                                                                 export=export)

            # si la requête sparql s'est faite sans problèmes, traduire les résultats en chaîne de caractères
            # pour les passer dans l'URL et pouvoir les récupérer dans un dictionnaire ; ensuite, rediriger vers
            # une page pour télécharger les résultats
            if len(err) == 0:
                flash("La requête s'est exécutée sans problèmes; vous pouvez télécharger vos fichiers.", "success")
                querystr = "{\"datadict\": " + str(datadict) + ", " \
                           + "\"queryname\": " + "\"" + queryname + "\"" + ", "\
                           + "\"outname\": " + "\"" + outname + "\"" + "}"
                querystr = quote_plus(querystr)
                return redirect(url_for("sparql_results", querystr=querystr))
            else:
                erreurs.append(err)
                erreurs = "~".join(str(e) for e in erreurs)
                erreurs = str(erreurs)
                flash(erreurs, "error")
                return render_template("pages/duchamp_sparqler.html",
                                       erreurs=erreurs, artistes=artistes, last_nominations=last_nominations,
                                       last_artistes=last_artistes, last_galeries=last_galeries,
                                       last_themes=last_themes, last_villes=last_villes)

        else:
            erreurs = "~".join(e for e in erreurs)
            erreurs = str(erreurs)
            flash(erreurs, "error")
            return render_template("pages/duchamp_sparqler.html",
                                   erreurs=erreurs, artistes=artistes, last_nominations=last_nominations,
                                   last_artistes=last_artistes, last_galeries=last_galeries,
                                   last_themes=last_themes, last_villes=last_villes)

    # return
    if len(erreurs) > 0:
        erreurs = str(erreurs)
        flash(erreurs, "error")
    else: erreurs = ""
    return render_template("pages/duchamp_sparqler.html", erreurs=erreurs,
                           artistes=artistes, last_nominations=last_nominations, last_artistes=last_artistes,
                           last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


@app.route("/duchamp_sparqler/results/<querystr>")
def sparql_results(querystr):
    """Route permettant d'afficher et de télécharger les résultats d'une requête SPARQL.

    :param querystr: requête HTTP encodée qui correspond à un objet JSON contenant les résultats de la requête
    :return: si une requête a été lancée, render_template vers une page affichant les résultats et permettant
             de les télécharger. sinon, redirection vers l'accueil avec un message d'erreur.
    :rtype: render_template si tout va bien, redirect sinon
    """
    # si une requête a été lancée, récupérer la requête et la traduire en json
    if querystr != "":
        querystr = unquote_plus(querystr)
        querystr = querystr.replace("'", "\"")
        querystr = json.loads(querystr)
        datadict = querystr["datadict"]
        queryname = querystr["queryname"]
        outname = querystr["outname"]
        name = datadict["labelen"]
        return render_template("pages/duchamp_sparqler_out.html", datadict=datadict, queryname=queryname,
                               outname=outname, name=name, last_nominations=last_nominations,
                               last_artistes=last_artistes, last_galeries=last_galeries, last_themes=last_themes,
                               last_villes=last_villes)
    # sinon, rediriger vers la page d'accueil avec un message d'erreur
    else:
        flash("Vous devez lancer une requête sparql avant de pouvoir récupérer des résultats", "error")
        return redirect("/")


@app.route("/duchamp_sparqler/results")
def sparql_results_without_req():
    """Route redirigeant sur la page d'accueil si on arrive à la page des résultats sans avoir lancé de requête."""
    flash("Vous devez lancer une requête sparql avant de pouvoir récupérer des résultats", "error")
    return redirect("/")


# ----- ROUTES UTILITAIRES ----- #
@app.route("/carte_ville/<int:id>")
def carte_ville(id):
    """Route permettant d'appeler une carte à intégrer dans un iframe dans une page HTML"""
    return render_template(f"partials/maps/ville{id}.html")


@app.route("/carte_artiste/<int:id>")
def carte_artiste(id):
    """Route permettant d'appeler une carte à intégrer dans un iframe dans une page HTML"""
    return render_template(f"partials/maps/artiste{id}.html")


@app.route("/carte_galerie/<int:id>")
def carte_galerie(id):
    """Route permettant d'appeler une carte à intégrer dans un iframe dans une page HTML"""
    return render_template(f"partials/maps/galerie{id}.html")


@app.route("/download/<filename>")
def dl(filename):
    try:
        return send_file(os.path.join(uploads, filename), as_attachment=True)
    except Exception as error:
        # si le fichier n'est plus disponible, faire une redirection
        erreurs = f"Ce fichier n'est plus disponible. Veuillez relancer la requête pour le télécharger\
                    ~{error}"
        flash(erreurs, "error")
        return render_template("pages/duchamp_sparqler_out.html", erreurs=erreurs,
                               last_nominations=last_nominations, last_artistes=last_artistes,
                               last_galeries=last_galeries, last_themes=last_themes, last_villes=last_villes)


@app.route("/sparql")
def sparql_redirect():
    """Route permettant la redirection vers la bonne URL"""
    return redirect("/duchamp_sparqler")


@app.route("/sparql/results")
def sparql_results_redirect():
    """Route permettant la redirection vers la bonne URL"""
    return redirect("/duchamp_sparqler/results")