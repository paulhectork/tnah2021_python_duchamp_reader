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
        # vérifier que toutes les données ont été fournies ; l'ajout d'un id wikidata n'est pas obligartoire
        laureat = bool(laureat)
        erreurs = []
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
        if annee_naissance:
            annee_naissance = int(annee_naissance.strip())
        if annee_nomination:
            annee_nomination = int(annee_nomination.strip())
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
        if not isinstance(annee_naissance, int):
            erreurs.append("La date de naissance ne doit contenir que des chiffres")
        if len(str(annee_nomination)) != 4:
            erreurs.append("L'année de nomination  doit être au format: AAAA")
        if not isinstance(annee_nomination, int):
            erreurs.append("L'année de nomination ne doit contenir que des chiffres")
        if id_wikidata:
            wikiregex = re.search(regexwkd, id_wikidata)
            if not wikiregex:
                erreurs.append("Un identifiant wikidata correspond à la forme suivante : \
                Q suivi de un ou plusieurs chiffres")
            id_wiki_check = Artiste.query.filter(Artiste.id_wikidata == id_wikidata).count()
            if id_wiki_check > 0:
                erreurs.append("Cet identifiant wikipedia existe déjà ; veuillez en choisir un autre.")

        # vérifier si l'artiste existe déjà dans la base de données ou si il/elle a déjà une nomination à son nom
        db_artiste_check = Artiste.query.filter(db.and_(
            Artiste.nom == nom,
            Artiste.prenom == prenom
        )).count()
        if db_artiste_check > 0:
            erreurs.append("Cet.te artiste existe déjà dans la base; veuillez changer le nom ou le prénom de l'artiste \
            pour ajouter un.e nouvel.le artiste à la base")
        db_artiste_check = Artiste.query.filter(db.and_(
            Artiste.prenom == prenom,
            Artiste.nom == nom
        )).first()
        if db_artiste_check:
            db_nomination_check = Nomination.query.filter(
                Nomination.id_artiste == db_artiste_check.id
            ).count()
            if db_nomination_check > 0:
                erreurs.append("Cet.te artiste a déjà une nomination enregistrée dans la base de données.")

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

    # une version très allégée de artiste_new() pour ajouter des données au moment de l'initialisation de la base
    @staticmethod
    def artiste_new_init(nom, prenom, annee_naissance, genre, id_wikidata, id_ville_naissance, id_ville_residence):
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
                    "Un identifiant wikidata correspond à l'expression: ^Q\d+$ (Q suivi de un ou plusieurs chiffres)")

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