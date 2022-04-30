from sqlalchemy.ext import hybrid

from ..app import db
from ..utils.regex import *
from ..utils.geography import coordinator

# les tables génériques
class Artiste(db.Model):
    __tablename__ = "artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text, nullable=False)
    annee_naissance = db.Column(db.Integer) # format YYYY
    genre = db.Column(db.String(1))  # M : masculin, F : femme, A : autre/non-binaire
    id_wikidata = db.Column(db.Text)
    id_ville_naissance = db.Column(db.Integer, db.ForeignKey("ville.id"))
    id_ville_residence = db.Column(db.Integer, db.ForeignKey("ville.id"))
    classname = db.Column(db.Text, nullable=False, default="artiste")

    authorship = db.relationship("AuthorshipArtiste", back_populates="artiste")
    represent = db.relationship("RelationRepresente", back_populates="artiste")
    ville_naissance = db.relationship("Ville", foreign_keys=[id_ville_naissance],
                                      backref="artiste_ville_naissance", uselist=False)
    ville_residence = db.relationship("Ville", foreign_keys=[id_ville_residence],
                                      backref="artiste_ville_residence", uselist=False)
    nomination = db.relationship("Nomination", back_populates="artiste", uselist=False)

    @hybrid.hybrid_property
    def full(self):
        """Cette propriété permet de concaténer prénom et nom pour retourner un nom complet.

        :return: Nom complet
        :rtype: str
        """
        return self.prenom + " " + self.nom

    @staticmethod
    def artiste_new(nom, prenom, laureat, theme, annee_nomination, annee_naissance,
                    genre, ville_naissance, pays_naissance, ville_residence, pays_residence, id_wikidata):
        """Ajouter un.e nouvel.le artiste et nomination à la base de données. Si le thème indiqué n'existe pas,
        la fonction gère l'ajout à la table Theme. Si les villes indiquées n'existent pas, la fonction essaye
        de récupérer la longitude et la latitude de la ville et ajoute les villes à la table Ville. Les pays
        sont demandés pour récupérer les coordonnées de la ville avec geopy. Étant donné que les données de Nomination
        et de Artiste se recoupent pour beaucoup, la fonction artiste_new permet aussi de créer une nouvelle nomination.
        Il n'y a donc pas de fonction pour créer directement une nouvelle nomination.

        :param nom: nom de l'artiste. type str
        :param prenom: prénom de l'artiste. type str
        :param laureat: booléen indiquant si l'artiste est lauréat.e ou nominé.e. type bool
        :param theme: thème sur lequel travaille l'artiste. type str
        :param annee_nomination: année où l'artiste est nominé.e au prix Marcel Duchamp. type str ou int (retypé en int)
        :param annee_naissance: année où l'artiste est né.e. type str ou int (retypé en int)
        :param genre: genre de l'artiste. valeurs autorisées: A, F, M. type str
        :param ville_naissance: ville de naissance de l'artiste. type str
        :param pays_naissance: pays de naissance de l'artiste. type str
        :param ville_residence: ville de résidence de l'artiste. type str
        :param pays_residence: pays de résidence de l'artiste. type str
        :param id_wikidata: identifiant wikidata, facultatif. permet de lancer une requête wikidata. type str
        :return: si il n'y a pas d'erreur, nouvelle nomination après avoir rajouté toutes les tables nécessaires. Sinon,
        chaîne de caractères contenant toutes les erreurs.
        """
        # valider les données
        nom, prenom, genre, annee_naissance, annee_nomination, ville_naissance, ville_residence, \
        pays_naissance, pays_residence, theme, id_wikidata, laureat, erreurs = \
            validate_artiste(nom=nom, prenom=prenom, genre=genre, annee_naissance=annee_naissance,
                             annee_nomination=annee_nomination, ville_naissance=ville_naissance,
                             ville_residence=ville_residence, pays_naissance=pays_naissance,
                             pays_residence=pays_residence, theme=theme, id_wikidata=id_wikidata,
                             laureat=laureat)

        # vérifier qu'il n'y a pas d'erreurs dans l'ajout d'un nouvel artiste
        if len(erreurs) > 0:
            return False, erreurs

        # si les villes n'existent pas dans la base de données, essayer de récupérer
        # leurs coordonnées et les y rajouter ; si la ville de naissance est la même que la ville de résidence,
        # ne rajouter que la première ville
        if ville_naissance == ville_residence and pays_naissance == pays_residence:
            db_ville_check = Ville.query.filter(db.and_(
                Ville.nom == ville_naissance,
                Ville.pays == pays_naissance
            )).count()
            if db_ville_check == 0:
                longitude, latitude = coordinator(f"{ville_naissance}, {pays_naissance}")
                nv_ville = Ville(
                    nom=ville_naissance,
                    pays=pays_naissance,
                    longitude=longitude,
                    latitude=latitude
                )
                try:
                    db.session.add(nv_ville)
                    db.session.commit()
                except Exception as error:
                    return False, [str(error)]
        else:
            db_ville_n_check = Ville.query.filter(db.and_(
                Ville.nom == ville_naissance,
                Ville.pays == pays_naissance
            )).count()
            if db_ville_n_check == 0:
                longitude, latitude = coordinator(f"{ville_naissance}, {pays_naissance}")
                nv_ville = Ville(
                    nom=ville_naissance,
                    pays=pays_naissance,
                    longitude=longitude,
                    latitude=latitude
                )
                try:
                    db.session.add(nv_ville)
                    db.session.commit()
                except Exception as error:
                    return False, [str(error)]
            db_ville_r_check = Ville.query.filter(Ville.nom == ville_residence).count()
            if db_ville_r_check == 0:
                longitude, latitude = coordinator(f"{ville_residence}, {pays_residence}")
                nv_ville = Ville(
                    nom=ville_residence,
                    pays=pays_residence,
                    latitude=latitude,
                    longitude=longitude
                )
                try:
                    db.session.add(nv_ville)
                    db.session.commit()
                except Exception as error:
                    return False, [str(error)]

        # si il n'y a pas d'erreurs, récupérer les données nécessaires et ajouter un.e nouvel.le artiste à la base
        db_ville_naissance = Ville.query.filter(Ville.nom == ville_naissance).first()
        id_ville_naissance = db_ville_naissance.id
        db_ville_residence = Ville.query.filter(Ville.nom == ville_residence).first()
        id_ville_residence = db_ville_residence.id

        # ajouter l'artiste à la base de données
        nv_artiste = Artiste(
            nom=nom,
            prenom=prenom,
            genre=genre,
            annee_naissance=annee_naissance,
            id_wikidata=id_wikidata,
            id_ville_naissance=id_ville_naissance,
            id_ville_residence=id_ville_residence
        )
        try:
            db.session.add(nv_artiste)
            db.session.commit()
        except Exception as error:
            return False, [str(error)]

        # vérifier si le thème existe dans la bdd ; si il n'existe pas, l'ajouter à la base de données
        db_theme_check = Theme.query.filter(Theme.nom == theme).count()
        if db_theme_check == 0:
            nv_theme = Theme(nom=theme)
            try:
                db.session.add(nv_theme)
                db.session.commit()
            except Exception as error:
                return False, [str(error)]

        # récupérer les identifiants de l'artiste et du thème nécessaires et ajouter la nouvelle nomination à la BDD
        db_artiste = Artiste.query.filter(db.and_(
            Artiste.nom == nom,
            Artiste.prenom == prenom
        )).first()
        id_artiste = db_artiste.id
        db_theme = Theme.query.filter(Theme.nom == theme).first()
        id_theme = db_theme.id

        nv_nomination = Nomination(
            annee=annee_nomination,
            laureat=laureat,
            id_artiste=id_artiste,
            id_theme=id_theme
        )
        try:
            db.session.add(nv_nomination)
            db.session.commit()
            return True, nv_nomination
        except Exception as error:
            return False, [str(error)]
        # si cette fonction de l'angoisse fonctionne, prendre une pause méritée

    @staticmethod
    def artiste_new_init(nom, prenom, annee_naissance, genre, id_wikidata, id_ville_naissance, id_ville_residence):
        """
        fonction permettant d'ajouter les artistes lorsque la base de données est peuplée au lancement de l'application
        :param nom: nom de l'artiste
        :param prenom: prénom de l'artiste
        :param annee_naissance: année de naissance de l'artiste
        :param genre: genre de l'artiste
        :param id_wikidata: identifiant wikidata
        :param id_ville_naissance: clé renvoyant à l'identifiant de la ville de naissance de l'artiste
        :param id_ville_residence: clé renvoyant à l'identifiant de la ville de résidence de l'artiste
        :return: True et objet sqlalchemy correspondant au nouvel artiste si tout va bien ; message d'erreur et False
        sinon
        """
        erreurs = []
        if not nom:
            erreurs.append("Un.e artiste doit avoir un nom")
        if not prenom:
            erreurs.append("Un.e artiste doit avoir un prénom")
        if not annee_naissance:
            erreurs.append("Un.e artiste doit avoir une date de naissance")
        if not genre:
            erreurs.append("Un.e artiste doit avoir un genre")
        if not id_ville_naissance:
            erreurs.append("Vous devez fournir la ville de naissance de votre artiste")
        if not id_ville_residence:
            erreurs.append("Vous devez fournir la ville de résidence de votre artiste")

        # vérification des données
        nom = clean_string(nom)
        prenom = clean_string(prenom)
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append("Nom incorrect. Voir regex")
        prenomregex = re.search(regexnp, prenom)
        if not prenomregex:
            erreurs.append("Prenom incorrect. Voir regex")
        if len(str(annee_naissance)) != 4:
            erreurs.append("La date de naissance doit être au format: AAAA")
        if not isinstance(annee_naissance, int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
        genres_autorises = ["A", "F", "M"]
        if genre not in genres_autorises:
            erreurs.append("Le genre doit être A, F ou M")
        if id_wikidata:
            wikiregex = re.search(regexwkd, id_wikidata)
            if not wikiregex:
                erreurs.append(
                    "Un identifiant wikidata correspond à l'expression: ^Q\d+$ (Q suivi de un ou plusieurs chiffres)"
                )

        # si tout va bien, on ajoute les données
        if len(erreurs) > 0:
            return False, erreurs
        # le code arrête de marcher là on dirait: ça doit return false ?
        nv_artiste = Artiste(
            nom=nom,
            prenom=prenom,
            genre=genre,
            annee_naissance=annee_naissance,
            id_wikidata=id_wikidata,
            id_ville_naissance=id_ville_naissance,
            id_ville_residence=id_ville_residence
        )
        try:
            db.session.add(nv_artiste)
            db.session.commit()
            return True, nv_artiste
        except Exception as error:
            return False, [str(error)]


class Nomination(db.Model):
    __tablename__ = "nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    annee = db.Column(db.Integer, nullable=False) # format YYYY
    laureat = db.Column(db.Boolean, nullable=False, default=0) # 1 si lauréat, 0 si non
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"), nullable=False)
    id_theme = db.Column(db.Integer, db.ForeignKey("theme.id"), nullable=False)
    classname = db.Column(db.Text, nullable=False, default="nomination")

    authorship = db.relationship("AuthorshipNomination", back_populates="nomination")
    artiste = db.relationship("Artiste", back_populates="nomination")
    theme = db.relationship("Theme", back_populates="nomination", uselist=False)

    @staticmethod
    def nomination_new_init(annee, laureat, id_artiste, id_theme):
        """
        fonction permettant d'ajouter les nominations lors de la création de la base de données au premier
        lancement de l'application
        :param annee: année de nomination
        :param laureat: booléen indiquant si l'artiste est lauréat.e ou non
        :param id_artiste: clé renvoyant à l'identifiant de l'artiste
        :param id_theme: clé renvoyant au thème de l'artiste
        :return: True & objet sqlalchemy correspondant à la nouvelle nomination si tout va bien ; erreur & False sinon
        """
        erreurs = []
        if not annee:
            erreurs.append("Fournir une année")
        if not id_artiste:
            erreurs.append("Fournir un id d'artiste")
        if not id_theme:
            erreurs.append("Fournir un id de theme")

        # nettoyer les données et vérifier leur validité
        if len(str(annee)) != 4:
            erreurs.append("La date de naissance doit être au format: AAAA")
        if not isinstance(annee, int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
        if not isinstance(laureat, bool):
            erreurs.append("Le lauréat est un BOOL (1: Oui, 0: Non)")
        if not isinstance(id_artiste, int):
            erreurs.append("L'id_artiste doit être un integer")
        if not isinstance(id_theme, int):
            erreurs.append("L'id_theme doit être un integer")

        # si tout va bien, on rajoute les données
        if len(erreurs) > 0:
            print(erreurs)
            return False, erreurs
        nv_nomination = Nomination(
            annee=annee,
            laureat=laureat,
            id_artiste=id_artiste,
            id_theme=id_theme
        )
        try:
            db.session.add(nv_nomination)
            db.session.commit()
            return True, nv_nomination
        except Exception as error:
            return False, [str(error)]


class Galerie(db.Model):
    __tablename__ = "galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, unique=True, nullable=False)
    url = db.Column(db.Text, unique=True)
    classname = db.Column(db.Text, nullable=False, default="galerie")

    authorship = db.relationship("AuthorshipGalerie", back_populates="galerie")
    represent = db.relationship("RelationRepresente", back_populates="galerie")
    localisation = db.relationship("RelationLocalisation", back_populates="galerie")

    @staticmethod
    def galerie_new(nom, url):
        """
        fonction permettant d'ajouter une galerie à la base de données
        :param nom: nom de la galerie
        :param url: url de la galerie
        :return: True et objet sqlalchemy correspondant à la nouvelle galerie si tout va bien ; sinon, False et
        message d'erreur
        """
        nom, url, erreurs = validate_galerie(nom=nom, url=url)

        # si il y a des erreurs, arrêter ; si tout va bien, ajouter la galerie à la base de données
        if len(erreurs) > 0:
            return False, erreurs
        nv_galerie = Galerie(
            nom=nom,
            url=url
        )
        try:
            db.session.add(nv_galerie)
            db.session.commit()
            return True, nv_galerie
        except Exception as error:
            return False, [str(error)]

    @staticmethod
    def galerie_new_init(nom, url):
        """
        fonction permettant de peupler la base de données lors du premier lancement de l'application
        :param nom: nom de la galerie
        :param url: url de la galerie
        :return: nom et url nettoyés, liste d'erreurs (vide si il n'y a pas d'erreurs)
        """
        # vérifier la validité des données
        nom, url, erreurs = validate_galerie(nom=nom, url=url)

        # vérifier si il y a des erreurs; sinon, rajouter les données à la base
        if len(erreurs) > 0:
            print(erreurs)
            return False, erreurs
        nv_galerie = Galerie(
            nom=nom,
            url=url
        )
        try:
            db.session.add(nv_galerie)
            db.session.commit()
            return True, nv_galerie
        except Exception as error:
            return False, [str(error)]


class Ville(db.Model):
    __tablename__ = "ville"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)  # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    longitude = db.Column(db.Float)  # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    pays = db.Column(db.Text, nullable=False)
    classname = db.Column(db.Text, nullable=False, default="ville")

    authorship = db.relationship("AuthorshipVille", back_populates="ville")
    localisation = db.relationship("RelationLocalisation", back_populates="ville")

    @staticmethod
    def ville_new(nom, latitude, longitude, pays):
        """
        fonction permettant d'ajouter une nouvelle ville à la base de données
        :param nom: nom de la ville
        :param latitude: latitude de la ville
        :param longitude: longitude de la ville
        :param pays: pays où se trouve la ville
        :return: True et objet sqlalchemy correspondant à la nouvelle ville si tout va bien ; sinon, False et message
        d'erreur
        """
        nom, longitude, latitude, pays, erreurs = validate_ville(nom=nom, longitude=longitude,
                                                                 latitude=latitude, pays=pays)

        if len(erreurs) > 0:
            return False, erreurs

        # si tout va bien, ajouter la ville à la base de données
        nv_ville = Ville(
            nom=nom,
            latitude=latitude,
            longitude=longitude,
            pays=pays
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville
        except Exception as error:
            return False, [str(error)]

    @staticmethod
    def ville_new_init(nom, latitude, longitude, pays):
        """
        fonction permettant de peupler la table Ville lors de la création de la base de données
        :param nom: nom de la ville
        :param latitude: latitude de la ville
        :param longitude: longitude de la ville
        :param pays: pays où se trouve la ville
        :return: True et objet sqlalchemy correspondant à la nouvelle ville si tout va bien ; sinon, False et message
        d'erreur
        """
        # vérifier la validité des données et les nettoyer
        nom, longitude, latitude, pays, erreurs = validate_ville(nom=nom, longitude=longitude,
                                                                 latitude=latitude, pays=pays)

        # vérifier si il y a des erreurs; sinon, ajouter les données à la base
        if len(erreurs) > 0:
            return False, erreurs
        nv_ville = Ville(
            nom=nom,
            latitude=latitude,
            longitude=longitude,
            pays=pays
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville
        except Exception as error:
            return False, [str(error)]

    @hybrid.hybrid_property
    def full(self):
        """Cette propriété permet de concaténer nom de la ville et nom du pays.
        :return: Nom de la ville avec nom du pays entre parenthèses
        :rtype: str
        """
        return self.nom + " (" + self.pays + ")"


class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    classname = db.Column(db.Text, nullable=False, default="theme")

    authorship = db.relationship("AuthorshipTheme", back_populates="theme")
    nomination = db.relationship("Nomination", back_populates="theme")

    @staticmethod
    def theme_new(nom):
        """
        fonction permettant de créer un nouveau thème
        :param nom: nom du thème
        :return: True et objet sqlalchemy correspondant au thème si tout va bien. sinon, False et liste d'erreurs
        """
        # vérifier la validité des données
        nom, erreurs = validate_theme(nom=nom)

        if len(erreurs) > 0:
            return False, erreurs

        # si tout va bien, rajouter les données à la base de données
        nv_theme = Theme(
            nom=nom
        )
        try:
            db.session.add(nv_theme)
            db.session.commit()
            return True, nv_theme
        except Exception as error:
            return False, [str(error)]

    @staticmethod
    def theme_new_init(nom):
        """
        fonction permettant de peupler la table Theme à l'initialisation de la base de données
        :param nom: nom du thème
        :return: True et objet sqlalchemy correspondant au thème si tout va bien; False et message d'erreur sinon
        """
        # vérifier la validité des données
        nom, erreurs = validate_theme(nom=nom)

        # si il n'y a pas d'erreurs, ajouter les données à la base
        if len(erreurs) > 0:
            return False, erreurs
        nv_theme = Theme(
            nom=nom
        )
        try:
            db.session.add(nv_theme)
            db.session.commit()
            return True, nv_theme
        except Exception as error:
            return False, [str(error)]


# ----- ÉVITER LES IMPORTS CIRCULAIRES ----- #
from ..utils.validation import validate_artiste, validate_galerie, validate_ville, validate_theme