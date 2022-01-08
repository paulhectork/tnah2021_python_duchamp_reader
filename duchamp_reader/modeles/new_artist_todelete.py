from .. import db
from regex import *

# POUR TOUT CE QUI N'EST PAS DES STRINGS, FAIRE ISINSTANCE()
# SQLite (pas sqlalchemy) fait la conversion automatique des datatypes tradi SQL (varchar, date...) en datatypes SQLite
# staticmethod de la classe Artiste
# ATTENTION AUX ERREURS DE TYPAGE !!

@staticmethod
def artiste_new(nom, prenom, annee_naissance, genre, ville_naissance, ville_residence):
    # vérifier que toutes les données ont été fournies
    erreurs = []
    if not nom:
        erreurs.append("Un.e artiste doit avoir un nom")
    if not prenom:
        erreurs.append("Un.e artiste doit avoir un prénom")
    if not annee_naissance:
        erreurs.append("Un.e artiste doit avoir une date de naissance")
    if not genre:
        erreurs.append("Un.e artiste doit avoir un genre")
    if not ville_naissance:
        erreurs.append("Vous devez fournir la ville de naissance de votre artiste")
    if not ville_residence:
        erreurs.append("Vous devez fournir la ville de résidence de votre artiste")

    # retirer les espaces superflus en début et fin des chaînes de caractères
    nom = clean_string(nom)
    prenom = clean_strip(prenom)
    # genre = je fais de genre une liste dans le formulaire donc jsp encore
    ville_naissance = clean_string(ville_naissance)
    ville_residence = clean_string(ville_residence)
    # je fais pas ça à date, vu que date sera un INT

    # vérifier que les données fournies sont correctes
    nomregex = re.search(regexnp, nom)
    if not nomregex:
        erreurs.append(
            "Un nom correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
        )
    prenomregex = re.search(regexnp, prenom)
    if not prenomregex:
        erreurs.append(
            "Un prénom correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
        )
    if len(str(annee_naissance)) != 4:
        erreurs.append("La date de naissance doit être au format: AAAA")
    if not isinstance(annee_naissance, int):
        erreurs.append("La date de naissance ne doit contenir que des chiffres")
    genres_autorises = ["A", "F", "M"]
    if genre not in genres_autorises:
        erreurs.append("Veulliez indiquer un genre correct: M pour masculin, F pour féminin, A pour autre ou non-binaire")
    # avec la ligne au dessus, il n'y a pas besoin de faire if len(genre)>1, ni de vérifier le datatype

    ville_n_regex = re.search(regexnp, ville_naissance)
    if not ville_n_regex:
        erreurs.append(
            "Un nom de ville de naissance correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
            (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
        )
    ville_r_regex = re.search(regexnp, ville_residence)
    if not ville_r_regex:
        erreurs.append(
                "Un nom de ville de résidence correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
            )

    db_artiste_check = Artiste.query.filter(db.and_(
            Artiste.nom == nom_artiste,
            Artiste.prenom == prenom_artiste
            )
        ).count()
    if db_artiste_check > 0:
        erreurs.append("Cet.te artiste existe déjà dans la base; veuillez changer le nom ou le prénom de l'artiste pour ajouter un.e nouvel.le artiste à la base")

    # vérifier qu'il n'y a pas d'erreurs dans l'ajout d'un nouvel artiste
    if len(erreurs) > 0:
        return False, erreurs

    # ma politique dans l'ajout de données sur tableA qui implique l'ajout de donnée sur tableB : l'ajout de données est seult obligatoire quand on ajoute les données sur la table principale (tableA), pas sur la table secondaire (tableB)
    db_ville_n_check = Ville.query.filter(Ville.nom == ville_naissance).count()
    if db_ville_n_check == 0:
        nv_ville = Ville(
            nom=ville_naissance
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville  # on est pas obligés de retourner l'objet, mais ça mange pas de pain ; faut-il mettre un return, ou est-ce que ça risque de baiser tte la fonction ?
        except Exception as error:
            return False, [str(error)]
    db_ville_r_check = Ville.query.filter(Ville.nom == ville_residence).count()
    if db_ville_r_check == 0:
        nv_ville = Ville(
            nom=ville_residence
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
        except Exception as error:
            return False, [str(error)]

    # si il n'y a pas d'erreurs, créer un.e nouvel.le artiste et l'ajouter à la base
    db_ville_naissance = Ville.query.filter(Ville.nom == ville_naissance).first()
    id_ville_naissance = db_ville_naissance.id
    db_ville_residence = Ville.query.filter(Ville.nom == ville_residence).first()
    id_ville_residence = db_ville_residence.id

    nv_artiste = Artiste(
        nom=nom,
        prenom=prenom,
        genre=genre,
        annee_naissance=annee_naissance,
        id_ville_naissance=id_ville_naissance,
        id_ville_residence=id_ville_residence
    )

    try:
        db.session.add(nv_artiste)
        db.session.commit()
        return True, nv_artiste
    except Exception as error:
        return False, [str(error)]