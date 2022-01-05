# POUR TOUT CE QUI N'EST PAS DES STRINGS, FAIRE ISINSTANCE()
# SQLite (pas sqlalchemy) fait la conversion automatique des datatypes tradi SQL (varchar, date...) en datatypes SQLite
# staticmethod de la classe Artiste
@staticmethod
def artiste_new(nom, prenom, date_naissance, genre, ville_naissance, ville_residence):
    # vérifier que toutes les données ont été fournies
    erreurs = []
    if not nom:
        erreurs.append("Un.e artiste doit avoir un nom")
    if not prenom:
        erreurs.append("Un.e artiste doit avoir un prénom")
    if not date_naissance:
        erreurs.append("Un.e artiste doit avoir une date de naissance")
    if not genre:
        erreurs.append("Un.e artiste doit avoir un genre")
    if not ville_naissance:
        erreurs.append("Vous devez fournir la ville de naissance de votre artiste")
    if not ville_residence:
        erreurs.append("Vous devez fournir la ville de résidence de votre artiste")

    # vérifier que les données fournies sont correctes
    genres_autorises = ["A", "F", "M"]
    if genre not in genres_autorises:
        erreurs.append(
            "Veulliez indiquer un genre correct: M pour masculin, F pour féminin, A pour autre ou non-binaire")
    # avec la ligne au dessus, il n'y a pas besoin de faire if len(genre)>1
    if len(date_naissance) > 4:
        erreurs.append("La date de naissance doit être au format: AAAA")
    if isinstance(date_naissance, int):
        erreurs.append("La date de naissance de doit contenir que des chiffres")

    # vérifier que le.a même artiste (ayant le même nom et prénom) n'existe pas déjà dans
    # la base
    nom_check = Artiste.query.filter(Artiste.nom == nom).count()
    prenom_check = Artiste.query.filter(Artiste.prenom == prenom).count()
    if prenom_check > 0 and nom_check > 0:
        erreurs.append(
            "Cet.te artiste existe déjà dans la base; veuillez changer le nom ou le prénom de l'artiste pour ajouter un.e nouvel.le artiste à la base")

    # vérifier qu'il n'y a pas d'erreurs dans l'ajout d'un nouvel artiste
    if len(erreurs) > 0:
        return False, erreurs

    # le problème pour faire des insertions dans une table avec des relations vers une autre:
    # faire une requête pour vérifier si les données destinées à la table externe (ville_naissance, ville_residence) existent déjà
    # comme on fait avec les artistes ou noms d'utilisateurs
    # si elles n'existent pas, on fait un commit avec ces données
    # ensuite, stocker l'ID des villes liées au nv artiste dans des variables (id_v_naissance, id_v_residence)
    # et utiliser ces variables dans le nv artiste
    # mais dans ce cas, il faudrait faire un nullable=False dans la table ville, vu qu'on ajoute pas toutes les données
    # CF CI-DESSOUS:

    # vérifier si les villes de naissance et de résidence existent ; si elles n'existent pas, les rajouter à la base de données:
    # MAIS ALORS EST-CE QUE LÀ ON RISQUE D'AVOIR DES PBS AVEC L'AJOUT DE VILLE AVANT LA DÉCLARATION DE LA CLASSE VILLE ???
    ville_naissance_check = Ville.query.filter(Ville.nom == ville_naissance).count()
    if len(ville_naissance_check) > 0:
        nv_ville = Ville(
            nom=ville_naissance
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville  # on est pas obligés de retourner l'objet, mais ça mange pas de pain ; faut-il mettre un return, ou est-ce que ça risque de baiser tte la fonction ?
        except Exception as error:
            return False, [str(error)]
    ville_residence_check = Ville.query.filter(Ville.nom == ville_residence).count()
    if len(ville_residence_check) > 0:
        nv_ville = Ville(
            nom=ville_residence
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville  # on est pas obligés de retourner l'objet, NE PAS POSER DE RETURN, ÇA MET FIN À LA FONCTION ; VOIR SI ON PEUT UTILISER YIELD À LA PLACE, mais ça transforme la fonction en générateur
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
        date_naissance=date_naissance,
        id_ville_naissance=id_ville_naissance,
        id_ville_residence=id_ville_residence
    )

    try:
        db.session.add(nv_artiste)
        db.session.commit()
        return True, nv_artiste
    except Exception as error:
        return False, [str(error)]