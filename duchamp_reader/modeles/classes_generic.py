import datetime

from ..app import db
from ..regex import *

# les tables de relation : tables d'Authorship, Represente(Artiste-Galerie), Localisation(Galerie-Ville)
class Authorship_Artiste(db.Model):
    __tablename__ = "authorship_artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    user = db.relationship("User", back_populates="authorships_artiste")
    artiste = db.relationship("Artiste", back_populates="authorships")


class Authorship_Nomination(db.Model):
    __tablename__ = "authorship_nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_nomination = db.Column(db.Integer, db.ForeignKey("nomination.id"))
    user = db.relationship("User", back_populates="authorships_nomination")
    nomination = db.relationship("Nomination", back_populates="authorships")


class Authorship_Galerie(db.Model):
    __tablename__ = "authorship_galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    user = db.relationship("User", back_populates="authorships_galerie")
    galerie = db.relationship("Galerie", back_populates="authorships")


class Authorship_Ville(db.Model):
    __tablename__ = "authorship_ville"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_ville = db.Column(db.Integer, db.ForeignKey("ville.id"))
    user = db.relationship("User", back_populates="authorships_ville")
    ville = db.relationship("Ville", back_populates="authorships")


class Authorship_Theme(db.Model):
    __tablename__ = "authorship_theme"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_theme = db.Column(db.Integer, db.ForeignKey("theme.id"))
    user = db.relationship("User", back_populates="authorships_theme")
    theme = db.relationship("Theme", back_populates="authorships")


class Represente(db.Model):
    __tablename__ = "represente"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    id_galerie =  db.Column(db.Integer, db.ForeignKey("galerie.id"))
    artiste = db.relationship("Artiste", back_populates="represents")
    galerie = db.relationship("Galerie", back_populates="represents")


class Localisation(db.Model):
    __tablename__ = "localisation"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    id_ville = db.Column(db.Integer, db.ForeignKey("ville.id"))
    galerie = db.relationship("Galerie", back_populates="localisations")
    ville = db.relationship("Ville", back_populates="localisations")



# les autres tables
class Artiste(db.Model):
    __tablename__ = "artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text, nullable=False)
    annee_naissance = db.Column(db.Integer) #format YYYY
    genre = db.Column(db.String(1)) # H : homme, F : femme, A : autre/non-binaire
    id_ville_naissance = db.Column(db.Integer, db.ForeignKey("ville.id"))
    id_ville_residence = db.Column(db.Integer, db.ForeignKey("ville.id"))

    authorships = db.relationship("Authorship_Artiste", back_populates="artiste")
    represents = db.relationship("Represente", back_populates="artiste")
    ville_residence = db.relationship("Ville", foreign_keys=[id_ville_residence], uselist=False)
    ville_naissance = db.relationship("Ville", foreign_keys=[id_ville_naissance], uselist=False)
    # j'ai un doute sur la classe où utiliser uselist=False pour le lien One-to-one entre Artiste et ville :
    # si on suit la doc SQLAlchemy pour la création de relations One to One, il faudrait placer uselist=False sur Ville
    # (ville n'a pas de clé externe), mais je veux que la relation scalaire soit de Artiste vers Ville (1 artiste = 1 ville), pas l'inverse
    nomination = db.relationship("Nomination", back_populates="artiste", uselist=False)

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

        # nettoyer les données et vérifier leur validité
        nom = clean_string(nom)
        prenom = clean_string(prenom)
        # genre = je fais de genre une liste dans le formulaire donc jsp encore
        ville_naissance = clean_string(ville_naissance)
        ville_residence = clean_string(ville_residence)
        # je fais pas ça à date, vu que date sera un INT
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
            erreurs.append(
                "Veulliez indiquer un genre correct: M pour masculin, F pour féminin, A pour autre ou non-binaire")
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
            Artiste.nom == nom,
            Artiste.prenom == prenom
        )).count()
        if db_artiste_check > 0:
            erreurs.append("Cet.te artiste existe déjà dans la base; veuillez changer le nom ou le prénom de l'artiste pour ajouter un.e nouvel.le artiste à la base")

        # vérifier qu'il n'y a pas d'erreurs dans l'ajout d'un nouvel artiste
        if len(erreurs) > 0:
            return False, erreurs

        # ma politique dans l'ajout de données sur tableA qui implique l'ajout de donnée sur tableB : l'ajout de données est seult obligatoire quand on ajoute les données sur la table principale (tableA), pas sur la table secondaire (tableB)
        db_ville_n_check = Ville.query.filter(Ville.nom == ville_naissance).count()
        if db_ville_n_check == 0:
            nv_ville = Ville(nom=ville_naissance)
            try:
                db.session.add(nv_ville)
                db.session.commit()
                return True, nv_ville  # on est pas obligés de retourner l'objet, mais ça mange pas de pain ; faut-il mettre un return, ou est-ce que ça risque de baiser tte la fonction ?
            except Exception as error:
                return False, [str(error)]
        db_ville_r_check = Ville.query.filter(Ville.nom == ville_residence).count()
        if db_ville_r_check == 0:
            nv_ville = Ville(nom=ville_residence)
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


class Nomination(db.Model):
    __tablename__ = "nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    annee = db.Column(db.Integer, nullable=False) # format YYYY
    laureat = db.Column(db.Boolean, nullable=False) # 1 si lauréat, 0 si non
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))

    authorships = db.relationship("Authorship_Nomination", back_populates="nomination")
    artiste = db.relationship("Artiste", back_populates="nomination")
    theme = db.relationship("Theme", back_populates="nominations", uselist = False)

    # COMMENT traduire le lauréat en booléen
    @staticmethod
    def nomination_new (annee, laureat, nom_artiste, prenom_artiste, theme):
        # vérifier que toutes les données ont été fournies
        erreurs = []
        if not annee:
            erreurs.append("Vous devez fournir une année de nomination")
        if not laureat:
            erreurs.append("Vous devez indiquer si l'artiste est lauréat.e ou non")
        if not nom_artiste:
            erreurs.append("Vous devez indiquer le nom de famille de l'artiste")
        if not prenom_artiste:
            erreurs.append("Vous devez indiquer le prénom de l'artiste")
        if not theme:
            erreurs.append("Vous devez indiquer le thème sur lequel travaille l'artiste")

        # nettoyer les données et vérifier leur validité
        nom_artiste = clean_string(nom_artiste)
        prenom_artiste = clean_string(prenom_artiste)
        theme = clean_string(theme).lower()
        if len(str(annee)) != 4:
            erreurs.append("La date de naissance doit être au format: AAAA")
        if not isinstance(annee, int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
        # pour lauréat j'y réfléchis plus tard
        nomregex = re.search(regexnp, nom_artiste)
        if not nomregex:
            erreurs.append(
                "Un nom correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
            )
        prenomregex = re.search(regexnp, prenom_artiste)
        if not prenomregex:
            erreurs.append(
                "Un prénom correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
            )
        themeregex = re.search(regexnc, theme)
        if not themeregex:
            erreurs.append(
                "Un nom de thème correspond à l'expression: ^(([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+(-|\s)?)([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+$ \
                (caractères en minuscules, accentués ou non, séparés ou non par un unique espace ou tiret)"
            )

        # LAUREAT
        # comment récupérer les données d'une liste à champ contrôlé ?
        # pour le lauréat, difficulté supplémentaire : dans le formulaire,
        # on a un champ <select><option>Oui</option><option>Non</option></select>, qui fait un choix dans une liste défilante ;
        # faut récupérer ces valeurs et les traduire en booléen

        # vérifier qu'il n'y ait pas d'erreurs
        if len(erreurs) > 0:
            return False, erreurs

        # vérifier si l'artiste et le thème existent ; sinon, les rajouter
        db_artiste_check = Artiste.query.filter(db.and_(
            Artiste.nom == nom_artiste,
            Artiste.prenom == prenom_artiste
        )).count()
        if db_artiste_check == 0:
            nv_artiste = Artiste(
                nom=nom_artiste,
                prenom=prenom_artiste
            )
            try:
                db.session.add(nv_artiste)
                db.session.commit()
            except Exception as error:
                return False, [str(error)]
        db_theme_check = Theme.query.filter(Theme.nom == theme).count()
        if db_theme_check == 0:
            nv_theme = Theme(
                nom=theme
            )
            try:
                db.session.add(nv_theme)
                db.session.commit()
            except Exception as error:
                return False, [str(error)]

        # si il n'y a pas d'erreurs, créer une nouvelle nomination et l'ajouter à la base
        # en fait je sais pas si on a besoin de récupérer toutes ces données sur d'autres tables
        db_artiste = Artiste.query.filter(db.and_(
            Artiste.nom == nom_artiste,
            Artiste.prenom == prenom_artiste
        )).first()
        id_artiste = db_artiste.id
        db_theme = Theme.query.filter(Theme.nom == theme).first() # EN FAIT JE CROIS PAS EN AVOIR BESOIN
        id_theme = db_theme.id # EN FAIT JE CROIS PAS EN AVOIR BESOIN

        nv_nomination = Nomination(
            annee=annee,
            laureat=laureat,
            id_artiste=id_artiste, # je croiiiiis
            id_theme=id_theme # je croiiiiiiis. plus globalement, est-ce que SQLAlchemy ajoute automatiquement les clés étrangères ?
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
    nom = db.Column(db.Text, nullable=False)

    authorships = db.relationship("Authorship_Galerie", back_populates="galerie")
    represents = db.relationship("Represente", back_populates="galerie")
    localisations = db.relationship("Localisation", back_populates="galerie")

    @staticmethod
    def galerie_new(nom):
        # vérifier que les données ont été fournies
        erreurs = []
        if not nom:
            erreurs.append("Une galerie doit avoir un nom")

        # nettoyer les données et vérifier leur validité
        nom = clean_string(nom)
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append(
                "Un nom de galerie correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
            )

        # vérifier si la galerie existe déjà dans la base de données
        db_galerie_check = Galerie.query.filter(Galerie.nom == nom).count()
        if db_galerie_check > 0:
            erreurs.append("Cette galerie existe déjà dans la base; veuillez changer le nom pour ajouter une nouvelle galerie à la base")

        if len(erreurs) > 0:
            return False, erreurs

        # si tout va bien, ajouter la galerie à la base de données
        nv_galerie = Galerie(nom=nom)
        try:
            db.session.add(nv_galerie)
            db.session.commit()
            return True, nv_galerie
        except Exception as error:
            return False, [str(error)]



class Ville(db.Model):
    __tablename__ = "ville"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, unique=True, nullable=False)
    longitude = db.Column(db.Float) # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    latitude = db.Column(db.Float) # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste

    authorships = db.relationship("Authorship_Ville", back_populates="ville")
    localisations = db.relationship("Localisation", back_populates="ville")
    artistes_ville_naissance = db.relationship("Artiste", back_populates="ville_naissance")
    artistes_ville_residence = db.relationship("Artiste", back_populates="ville_residence")

    @staticmethod
    def ville_new(nom, longitude, lattitude):
        # vérifier que les données ont été fournies
        erreurs = []
        if not nom:
            erreurs.append("Vous devez fournir un nom pour la ville")
        if not longitude:
            erreurs.append("Vous devez fournir une longitude pour cette ville")
        if not lattitude:
            erreurs.append("Vous devez fournir une lattitude pour cette ville")

        # nettoyer les données et vérifier leur validité
        nom = clean_string(nom)
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append(
                "Un nom de ville correspond à l'expression: ^[A-Z](([-\s][A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne)"
            )
        if not isinstance(longitude, float):
            erreurs.append("La longitude doit être un nombre décimal")
        if not isinstance(lattitude, float):
            erreurs.append("La lattitude doit être un nombre décimal")

        # vérifier que la ville n'existe pas déjà dans la  base de données
        db_ville_check = Ville.query.filter(db.and_(
            Ville.nom == nom,
            Ville.longitude == longitude,
            Ville.lattitude == lattitude
        )).count()
        if db_ville_check > 0:
            erreurs.append("Cette ville existe déjà ; veuillez changer le nom ou ses coordonnées pour rajouter une nouvelle ville à la base")

        if len(erreurs) > 0:
            return False, erreurs

        # si tout va bien, ajouter la ville à la base de données
        nv_ville = Ville(
            nom = nom,
            longitude = longitude,
            lattitude = lattitude
        )
        try:
            db.session.add(nv_ville)
            db.session.commit()
            return True, nv_ville
        except Exception as error:
            return False, [str(error)]


class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    id_nomination = db.Column(db.Text, db.ForeignKey("nomination.id"))

    authorships = db.relationship("Authorship_Theme", back_populates="theme")
    nominations = db.relationship("Nomination", back_populates="theme")
    # staticmethod de création de données



# les relations dont je suis assez sûr : toutes les tables de relation, la relation artiste-nomination, la relation artiste-theme
# là où j'ai un plus gros doute : les relations artiste-ville