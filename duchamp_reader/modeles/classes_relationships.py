from ..app import db
import datetime


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
