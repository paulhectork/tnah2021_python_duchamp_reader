from sqlalchemy.ext import hybrid

from ..app import db
from ..regex import *

# les tables génériques
class Artiste(db.Model):
    __tablename__ = "artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text, nullable=False)
    annee_naissance = db.Column(db.Integer) # format YYYY
    genre = db.Column(db.String(1))  # M : masculin, F : femme, A : autre/non-binaire
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
        ville_naissance = clean_string(ville_naissance)
        ville_residence = clean_string(ville_residence)
        annee_naissance = int(annee_naissance.strip())
        # je fais pas ça à date, vu que date sera un INT
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append(
                "Un nom correspond à l'expression: \
                ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        prenomregex = re.search(regexnp, prenom)
        if not prenomregex:
            erreurs.append(
                "Un prénom correspond à l'expression: ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        if len(str(annee_naissance)) != 4:
            erreurs.append("La date de naissance doit être au format: AAAA")
        if not isinstance(annee_naissance, int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
        ville_n_regex = re.search(regexnp, ville_naissance)
        if not ville_n_regex:
            erreurs.append(
                "Un nom de ville de naissance correspond à l'expression: \
                ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        ville_r_regex = re.search(regexnp, ville_residence)
        if not ville_r_regex:
            erreurs.append(
                "Un nom de ville de résidence correspond à l'expression: \
                ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )

        db_artiste_check = Artiste.query.filter(db.and_(
            Artiste.nom == nom,
            Artiste.prenom == prenom
        )).count()
        if db_artiste_check > 0:
            erreurs.append("Cet.te artiste existe déjà dans la base; veuillez changer le nom ou le prénom de l'artiste \
            pour ajouter un.e nouvel.le artiste à la base")

        # vérifier qu'il n'y a pas d'erreurs dans l'ajout d'un nouvel artiste
        if len(erreurs) > 0:
            return False, erreurs

        # ajouter les villes si elles n'existent pas dans la base de données
        db_ville_n_check = Ville.query.filter(Ville.nom == ville_naissance).count()
        if db_ville_n_check == 0:
            nv_ville = Ville(nom=ville_naissance)
            try:
                db.session.add(nv_ville)
                db.session.commit()
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

    # une version allégée de artiste_new() pour ajouter des données au moment de l'initialisation de la base
    @staticmethod
    def artiste_new_init(nom, prenom, annee_naissance, genre, id_ville_naissance, id_ville_residence):
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

        # si tout va bien, on ajoute les données
        if len(erreurs) > 0:
            return False, erreurs
        # le code arrête de marcher là on dirait: ça doit return false ?
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
    laureat = db.Column(db.Boolean, nullable=False, default=0) # 1 si lauréat, 0 si non
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"), nullable=False)
    id_theme = db.Column(db.Integer, db.ForeignKey("theme.id"), nullable=False)
    classname = db.Column(db.Text, nullable=False, default="nomination")

    authorship = db.relationship("AuthorshipNomination", back_populates="nomination")
    artiste = db.relationship("Artiste", back_populates="nomination")
    theme = db.relationship("Theme", back_populates="nomination", uselist=False)

    # COMMENT traduire le lauréat en booléen
    @staticmethod
    def nomination_new (annee, laureat, nom_artiste, prenom_artiste, theme):
        # vérifier que toutes les données ont été fournies
        erreurs = []
        if not annee:
            erreurs.append("Vous devez fournir une année de nomination")
        #  if not laureat:
        #    erreurs.append("Vous devez indiquer si l'artiste est lauréat.e ou non")
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
                "Un nom correspond à l'expression: ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        prenomregex = re.search(regexnp, prenom_artiste)
        if not prenomregex:
            erreurs.append(
                "Un prénom correspond à l'expression: ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        themeregex = re.search(regexnc, theme)
        if not themeregex:
            erreurs.append(
                "Un nom de thème doit correspondre à l'expression: \
                ^(([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])|(\-?\s?))+([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+$ \
                (minuscules uniquement, accentuées ou non, séparées par des espaces et/ou tirets)"
            )

        # LAUREAT
        # comment récupérer les données d'une liste à champ contrôlé ?
        # pour le lauréat, difficulté supplémentaire : dans le formulaire,
        # on a un champ <select><option>Oui</option><option>Non</option></select>,
        # qui fait un choix dans une liste défilante ;
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
        db_theme = Theme.query.filter(Theme.nom == theme).first()
        id_theme = db_theme.id

        nv_nomination = Nomination(
            annee=annee,
            laureat=laureat,
            id_artiste=id_artiste, # je croiiiiis
            id_theme=id_theme
        )
        try:
            db.session.add(nv_nomination)
            db.session.commit()
            return True, nv_nomination
        except Exception as error:
            return False, [str(error)]

    @staticmethod
    def nomination_new_init(annee, laureat, id_artiste, id_theme):
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
    # EUH? J'AI OUBLIÉ D'AJOUTER LA LOCALISATION ET QUI EST REPRÉSENTÉ PAR LA GALERIE
    # POUR FAIRE ÇA, IL FAUDRAIT GÉRER L'AJOUT DE DONNÉES AUX TABLES "RELATION_LOCALISATION"
    # ET "RELATION_REPRESENTE", CE QUI EN SOIT EST FAISABLE (mais doit être fait)
    def galerie_new(nom, url):
        # vérifier que les données ont été fournies
        erreurs = []
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

        # vérifier si la galerie existe déjà dans la base de données
        db_galerie_check = Galerie.query.filter(Galerie.nom == nom).count()
        if db_galerie_check > 0:
            erreurs.append("Cette galerie existe déjà dans la base; veuillez changer le nom pour ajouter une nouvelle \
            galerie à la base")

        if len(erreurs) > 0:
            return False, erreurs

        # si tout va bien, ajouter la galerie à la base de données
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
        erreurs = []
        if not nom:
            erreurs.append("Une galerie doit avoir un nom")
        if not url:
            erreurs.append("Vous devez fournir un URL")

        # nettoyer les données et vérifier leur validité
        nom = clean_string(nom)
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append("Nom incorrect. Voir regex")
        url = url.strip()
        urlregex = re.search(regexurl, url)
        if not urlregex:
            erreurs.append("URL incorrect. Voir regex")

        # vérifier si il y a des erreurs; sinon, rajouter les données à la base
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


class Ville(db.Model):
    __tablename__ = "ville"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, unique=True, nullable=False)
    latitude = db.Column(db.Float)  # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    longitude = db.Column(db.Float)  # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    pays = db.Column(db.Text)
    classname = db.Column(db.Text, nullable=False, default="ville")

    authorship = db.relationship("AuthorshipVille", back_populates="ville")
    localisation = db.relationship("RelationLocalisation", back_populates="ville")

    @staticmethod
    def ville_new(nom, latitude, longitude, pays):
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
        if not isinstance(longitude, float):
            erreurs.append("La longitude doit être un nombre décimal")
        if not isinstance(latitude, float):
            erreurs.append("La latitude doit être un nombre décimal")
        pays = clean_string(pays)
        paysregex = re.search(regexnp, pays)
        if not paysregex:
            erreurs.append(
                "Un nom de pays correspond à l'expression: \
                ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )

        # vérifier que la ville n'existe pas déjà dans la  base de données
        db_ville_check = Ville.query.filter(db.and_(
            Ville.nom == nom,
            Ville.longitude == longitude,
            Ville.latitude == latitude,
            Ville.pays == pays
        )).count()
        if db_ville_check > 0:
            erreurs.append("Cette ville existe déjà ; veuillez changer le nom ou ses coordonnées pour rajouter une \
            nouvelle ville à la base")

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
        # vérifier que toutes les données sont fournies
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
            erreurs.append("Nom non conforme à la regex")
        if not isinstance(longitude, float):
            erreurs.append("La longitude doit être un nombre décimal")
        if not isinstance(latitude, float):
            erreurs.append("La latitude doit être un nombre décimal")
        pays = clean_string(pays)
        paysregex = re.search(regexnp, nom)
        if not paysregex:
            erreurs.append("Nom de pays non conforme à la regex")

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
        # vérifier que les données sont fournies
        erreurs = []
        if not nom:
            erreurs.append("Vous devez fournir un nom")

        # nettoyer les données et vérifier leur validité
        nom = clean_string(nom)
        nomregex = re.search(regexnc, nom)
        if not nomregex:
            erreurs.append("Un nom de thème doit correspondre à l'expression: \
                ^^(([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])|(\-?\s?))+([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+$ \
                (minuscules uniquement, accentuées ou non, séparées par des espaces et/ou tirets)")
        nom = clean_string(nom).lower()

        # vérifier si le thème existe déjà dans la base de données
        db_theme_check = Theme.query.filter(Theme.nom == nom).count()
        if db_theme_check > 0:
            erreurs.append("Ce thème existe déjà; veuillez en fournir un autre")

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
        # vérifier que les données existent et qu'elles sont valides
        erreurs = []
        if not nom:
            erreurs.append("Fournir un nom")
        nomregex = re.search(regexnc, nom)
        if not nomregex:
            erreurs.append("Nom non conforme à la regex")
        nom = clean_string(nom).lower()

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

# les relations dont je suis assez sûr : toutes les tables de relation, la relation artiste-nomination, la relation
# artiste-theme
# là où j'ai un plus gros doute : les relations artiste-ville