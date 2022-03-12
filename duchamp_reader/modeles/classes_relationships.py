from ..app import db
import datetime


# les tables de relation : tables d'Authorship,
# RelationRepresente(Artiste-Galerie), RelationLocalisation(Galerie-Ville)
class AuthorshipArtiste(db.Model):
    __tablename__ = "authorship_artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    user = db.relationship("User", back_populates="authorship_artiste")
    artiste = db.relationship("Artiste", back_populates="authorship")


class AuthorshipNomination(db.Model):
    __tablename__ = "authorship_nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_nomination = db.Column(db.Integer, db.ForeignKey("nomination.id"))
    user = db.relationship("User", back_populates="authorship_nomination")
    nomination = db.relationship("Nomination", back_populates="authorship")


class AuthorshipGalerie(db.Model):
    __tablename__ = "authorship_galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    user = db.relationship("User", back_populates="authorship_galerie")
    galerie = db.relationship("Galerie", back_populates="authorship")


class AuthorshipVille(db.Model):
    __tablename__ = "authorship_ville"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_ville = db.Column(db.Integer, db.ForeignKey("ville.id"))
    user = db.relationship("User", back_populates="authorship_ville")
    ville = db.relationship("Ville", back_populates="authorship")


class AuthorshipTheme(db.Model):
    __tablename__ = "authorship_theme"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_theme = db.Column(db.Integer, db.ForeignKey("theme.id"))
    user = db.relationship("User", back_populates="authorship_theme")
    theme = db.relationship("Theme", back_populates="authorship")


class RelationRepresente(db.Model):
    __tablename__ = "relation_represente"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    artiste = db.relationship("Artiste", back_populates="represent")
    galerie = db.relationship("Galerie", back_populates="represent")

    # méthode de création de données à l'initialisation de la base
    @staticmethod
    def represente_new_init(id_artiste, id_galerie):
        # vérifier que les données sont fournies et valides
        erreurs = []
        if not id_artiste:
            erreurs.append("Fournir id_artiste")
        if not id_galerie:
            erreurs.append("Fournir id_galerie")
        if not isinstance(id_artiste, int):
            erreurs.append("id_artiste doit être un integer")
        if not isinstance(id_galerie, int):
            erreurs.append("id_galerie doit être un integer")

        # si tout va bien, ajouter les données à la classe
        if len(erreurs) > 0:
            return False, erreurs
        nv_represente = RelationRepresente(
            id_artiste=id_artiste,
            id_galerie=id_galerie
        )
        try:
            db.session.add(nv_represente)
            db.session.commit()
            return True, nv_represente
        except Exception as error:
            return False, [str(error)]


class RelationLocalisation(db.Model):
    __tablename__ = "relation_localisation"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    id_ville = db.Column(db.Integer, db.ForeignKey("ville.id"))
    galerie = db.relationship("Galerie", back_populates="localisation")
    ville = db.relationship("Ville", back_populates="localisation")

    @staticmethod
    def localisation_new_init(id_galerie, id_ville):
        # vérifier que les données sont fournies et valides
        erreurs = []
        if not id_ville:
            erreurs.append("Fournir id_ville")
        if not id_galerie:
            erreurs.append("Fournir id_galerie")
        if not isinstance(id_ville, int):
            erreurs.append("id_ville doit être un integer")
        if not isinstance(id_galerie, int):
            erreurs.append("id_galerie doit être un integer")

        # si tout va bien, ajouter les données à la classe
        if len(erreurs) > 0:
            return False, erreurs
        nv_localisation = RelationLocalisation(
            id_galerie=id_galerie,
            id_ville=id_ville
        )
        try:
            db.session.add(nv_localisation)
            db.session.commit()
            return True, nv_localisation
        except Exception as error:
            return False, [str(error)]
