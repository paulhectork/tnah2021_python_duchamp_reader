import re

from ..modeles.classes_generic import Artiste, Galerie, Ville, Theme
from .regex import clean_string, regexnp, regexnc, regexwkd, regexurl
from ..app import db

# fonctions permettant de valider les données pendant l'ajout / modification d'entrées dans la base de données

def validate_artiste(nom, prenom, genre, annee_naissance, annee_nomination, ville_naissance, ville_residence,
                    pays_naissance, pays_residence, theme, id_wikidata, laureat, id_artiste=None):
    """
    fonction permettant de valider les données avant un ajout / modification sur la table Artiste et Nomination.
    id_aritste est à utiliser pendant l'update.

    :param nom: nom de l'artiste
    :param prenom: prénom de l'artiste
    :param genre: genre de l'artiste
    :param annee_naissance: année de naissance de l'artiste
    :param annee_nomination: année de la nomination au prix Marcel Duchamp
    :param ville_naissance: ville de naissance de l'artiste
    :param ville_residence: ville de résidence de l'artiste
    :param pays_naissance: pays de naissance de l'artiste
    :param pays_residence: pays de résidence de l'artiste
    :param theme: thème sur lequel iel travaille
    :param id_wikidata: identifiant wikidata de l'artiste
    :param laureat: booléen indiquant si l'artiste est lauréat.e
    :param id_artiste: identifiant de l'artiste en cours de modification
    :return: toutes ces données nettoyées ainsi qu'une liste contenant des erreurs (liste vide si il n'y a pas d'erreur)
    """
    # vérifier que les données ont été fournies
    erreurs = []  # liste d'erreurs qui ont lieu au moment de l'ajout / modification des données
    if not nom:
        erreurs.append("Un.e artiste doit avoir un nom")
    if not prenom:
        erreurs.append("Un.e artiste doit avoir un prénom")
    if not annee_nomination:
        erreurs.append("Vous devez fournir une année de nomination")
    if not annee_naissance:
        erreurs.append("Un.e artiste doit avoir une date de naissance")
    if not genre:
        erreurs.append("Un.e artiste doit avoir un genre")
    if not ville_naissance:
        erreurs.append("Vous devez fournir la ville de naissance de votre artiste")
    if not ville_residence:
        erreurs.append("Vous devez fournir la ville de résidence de votre artiste")
    if not theme:
        erreurs.append("Vous devez indiquer le thème sur lequel travaille l'artiste")
    if not pays_naissance:
        erreurs.append("Vous devez fournir le pays de naissance de votre artiste")
    if not pays_residence:
        erreurs.append("Vous devez fournir le pays de résidence de votre artiste")
    if not theme:
        erreurs.append("Vous devez indiquer le thème sur lequel travaille l'artiste")

    # nettoyer les données et vérifier leur validité
    nom = clean_string(nom)
    prenom = clean_string(prenom)
    ville_naissance = clean_string(ville_naissance)
    pays_naissance = clean_string(pays_naissance)
    pays_residence = clean_string(pays_residence)
    ville_residence = clean_string(ville_residence)
    annee_naissance = annee_naissance.strip()
    annee_nomination = annee_nomination.strip()
    theme = clean_string(theme).lower()
    laureat = int(laureat)  # le laureat est retypé en integer et n'est pas travaillé plus
                            # que ça puisque la donnée n'est jamais librement entrée par l'utilisateurice
    if id_wikidata:
        id_wikidata = clean_string(id_wikidata)
    nomregex = re.search(regexnp, nom)
    if not nomregex:
        erreurs.append(
            "Un nom doit avoir la forme suivante : \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    prenomregex = re.search(regexnp, prenom)
    if not prenomregex:
        erreurs.append(
            "Un prénom doit avoir la forme suivante : \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    themeregex = re.search(regexnc, theme)
    if not themeregex:
        erreurs.append(
            "Un nom de thème doit avoir la forme suivante : \
            minuscules uniquement, accentuées ou non, séparées par des espaces et/ou tirets"
        )
    ville_n_regex = re.search(regexnp, ville_naissance)
    if not ville_n_regex:
        erreurs.append(
            "Un nom de ville doit avoir la forme suivante : \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    ville_r_regex = re.search(regexnp, ville_residence)
    if not ville_r_regex:
        erreurs.append(
            "Un nom de ville de résidence doit avoir la forme suivante: \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    pays_n_regex = re.search(regexnp, pays_naissance)
    if not pays_n_regex:
        erreurs.append(
            "Un nom de pays doit avoir la forme suivante : \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    pays_r_regex = re.search(regexnp, ville_residence)
    if not pays_r_regex:
        erreurs.append(
            "Un nom de pays de résidence doit avoir la forme suivante: \
            majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne"
        )
    if len(str(annee_naissance)) != 4:
        erreurs.append("La date de naissance doit être au format: AAAA")
    try:
        if not isinstance(int(annee_naissance), int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
    except:
        erreurs.append("La date de naissance ne doit contenir que des chiffres")
    if len(str(annee_nomination)) != 4:
        erreurs.append("L'année de nomination  doit être au format: AAAA")
    try:
        if not isinstance(int(annee_nomination), int):
            erreurs.append("L'année de nomination ne doit contenir que des chiffres")
    except:
        erreurs.append("L'année de nomination ne doit contenir que des chiffres")
    if id_wikidata:
        wikiregex = re.search(regexwkd, id_wikidata)
        if not wikiregex:
            erreurs.append("Un identifiant wikidata correspond à la forme suivante : \
             Q suivi de un ou plusieurs chiffres")
        id_wiki_check = Artiste.query.filter(db.and_(
            Artiste.id_wikidata == id_wikidata,
            Artiste.id != id_artiste
        )).count()
        if id_wiki_check > 0:
            erreurs.append("Cet identifiant wikipedia existe déjà ; veuillez en choisir un autre.")

    # return
    return nom, prenom, genre, annee_naissance, annee_nomination, ville_naissance, ville_residence, \
               pays_naissance, pays_residence, theme, id_wikidata, laureat, erreurs


def validate_galerie(nom, url, id_galerie=None):
    """
    fonction permettant vérifier que les données fournies à l'ajout / modification d'une galerie sont valides.
    id_galerie est à utiliser en cas de modification
    :param nom: nom de la galerie
    :param url: url du site web de la galerie
    :param id_galerie: identifiant de la galerie en cours de modification
    :return: nom de la galerie nettoyé, url de la galerie, liste d'erreurs (vide si il n'y a pas d'erreurs)
    """
    erreurs = []  # liste d'erreurs
    # vérifier que les données ont été fournies
    if not nom:
        erreurs.append("Une galerie doit avoir un nom")
    if not url:
        erreurs.append("Une galerie doit avoir un URL")

    # nettoyer les données et vérifier leur validité
    nom = clean_string(nom)
    nomregex = re.search(regexnp, nom)
    if not nomregex:
        erreurs.append(
            "Un nom de galerie correspond à l'expression: \
            ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne)"
        )
    url = url.strip()
    urlregex = re.search(regexurl, url)
    if not urlregex:
        erreurs.append(
            "Un URL correspond à l'expression: \
            http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.\
            Veuillez fournir un URL valide."
        )

    # vérifier si une galerie du même nom existe déjà dans la base de données
    db_galerie_check = Galerie.query.filter(db.and_(
            Galerie.nom == nom,
            Galerie.id != id_galerie
    )).count()
    if db_galerie_check > 0:
        erreurs.append("Cette galerie existe déjà dans la base; veuillez changer le nom pour ajouter une nouvelle \
                       galerie à la base")

    # return
    return nom, url, erreurs


def validate_ville(nom, longitude, latitude, pays, id_ville=None):
    """
    fonction permettant de valider et de corriger les données fournies pour la création / modification d'une
    ville dans la base de données. id_ville est à utiliser en cas de mise à jour
    :param nom: nom de la ville
    :param longitude: longitude de la ville
    :param latitude: latitude de la ville
    :param pays: pays où se trouve la ville
    :param id_ville: identifiant de la ville, à utiliser pendant les mises à jour
    :return: données corrigées et liste d'erreurs (vide si il n'y a pas d'erreurs)
    """
    # vérifier que les données ont été fournies
    erreurs = []
    if not nom:
        erreurs.append("Vous devez fournir un nom pour la ville")
    if not longitude:
        erreurs.append("Vous devez fournir une longitude pour cette ville")
    if not latitude:
        erreurs.append("Vous devez fournir une latitude pour cette ville")
    if not pays:
        erreurs.append("Vous devez fournir un pays pour cette ville")

    # nettoyer les données et vérifier leur validité
    nom = clean_string(nom)
    nomregex = re.search(regexnp, nom)
    if not nomregex:
        erreurs.append(
            "Un nom de ville correspond à l'expression: \
            ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne)"
        )
    pays = clean_string(pays)
    paysregex = re.search(regexnp, pays)
    if not paysregex:
        erreurs.append(
            "Un nom de pays correspond à l'expression: \
            ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
            tirets et espaces, miniscule en fin de chaîne)"
        )
    # vérifier que la longitude et la latitude sont valides
    try:
        longitude = re.sub(r",", ".", str(longitude)).strip()
        longitude = float(longitude)
        if not -180 <= longitude <= 180:
            erreurs.append("La longitude doit être un nombre décimal compris entre -180 et 180")
    except:
        erreurs.append("La longitude doit être un nombre décimal compris entre -180 et 180")
    try:
        latitude = re.sub(r",", ".", str(latitude)).strip()
        latitude = float(latitude)
        if not -90 <= latitude <= 90:
            erreurs.append("La latitude doit être un nombre décimal compris entre -90 et 90")
    except:
        erreurs.append("La latitude doit être un nombre décimal compris entre -90 et 90")

    # vérifier que la ville n'existe pas déjà dans la  base de données
    db_ville_check = Ville.query.filter(db.and_(
        Ville.nom == nom,
        Ville.longitude == longitude,
        Ville.latitude == latitude,
        Ville.pays == pays,
        Ville.id != id_ville
    )).count()
    if db_ville_check > 0:
        erreurs.append("Cette ville existe déjà ; veuillez changer le nom ou ses coordonnées pour rajouter une \
                nouvelle ville à la base")

    # return
    return nom, longitude, latitude, pays, erreurs


def validate_theme(nom, id_theme=None):
    """
    fonction permettant de nettoyer et de valider les données fournies à l'ajout / modification d'un thème.
    id_theme est à utiliser en cas de mise à jour
    :param nom: nom donné au thème
    :param id_theme: identifiant du thème (à utiliser pour l'update)
    :return: nom nettoyé et liste d'erreurs (si il n'y a pas d'erreurs, la liste est vide)
    """
    # vérifier que les données sont fournies
    erreurs = []
    if not nom:
        erreurs.append("Vous devez fournir un nom")

    # nettoyer les données et vérifier leur validité
    nom = clean_string(nom).lower()
    nomregex = re.search(regexnc, nom)
    if not nomregex:
        erreurs.append("Un nom de thème doit correspondre la forme suivante: \
                    minuscules uniquement, accentuées ou non, séparées par des espaces et/ou tirets")

    # vérifier si le thème existe déjà dans la base de données
    db_theme_check = Theme.query.filter(db.and_(
        Theme.nom == nom,
        Theme.id != id_theme
    )).count()
    if db_theme_check > 0:
        erreurs.append("Ce thème existe déjà; veuillez en fournir un autre")

    # return
    return nom, erreurs