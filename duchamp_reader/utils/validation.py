import re

from ..modeles.classes_generic import Artiste
from .regex import clean_string, regexnp, regexnc, regexwkd
from ..app import db

def validate_artist(nom, prenom, genre, annee_naissance, annee_nomination, ville_naissance, ville_residence,
                    pays_naissance, pays_residence, theme, id_wikidata, laureat, id_artiste=None):
    """
    fonction permettant de valider les données avant un ajout / modification sur la table Artiste et Nomination

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
    :param id_artiste: identifiant de l'artiste (pour l'update uniquement)
    :return: toutes ces données nettoyées ainsi qu'une liste contenant des erreurs (liste vide si il n'y a pas d'erreur)
    """
    # vérifier que les données ont été fournies
    erreurs = []  # liste d'erreurs qui ont lieu au moment de l'ajout / modification des données
    laureat = bool(laureat)
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