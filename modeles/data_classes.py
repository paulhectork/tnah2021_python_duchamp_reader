from flask import url_for
import datetime

#from .. import db #importer la base de données du duchamp_reader
# from users.py import User #on importe la classe user / ou alors ptet qu'on devra seult importer une partie
# ou alors rien du tout jsp

class Authorship(db.Model):
    __tablename__ = "authorship"
    id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # les liens vers les clés principales de toutes les autres tables qu'on peut modifier
    user = db.relationship("User", back_populates="authorships")
    # les db relationship qui permettent de créer des liens vers toutes les autres classes

# SQLite (pas sqlalchemy) fait la conversion automatique des datatypes tradi SQL (varchar, date...) en datatypes SQLite
class Artiste(db.Model):
    __tablename__ = "artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text, nullable=False)
    date_naissance = db.Column(db.Integer, nullable=False) # format YYYY - à rendre obligatoire dans la fonction de création de nv artistes avec des 'if...not'
    genre = db.Column(db.String(1)) # 3 caractères possibles à entrer dans les fonctions de création : A, F, M
    # les db.ForeignKey et db.relationship vers la table Authorship, représente, ville
    # staticmethod de création d'un nv artiste

class Nomination(db.Model):
    __tablename__ = "nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    laureat = db.Column(db.Boolean, nullable=False)
    # relation vers authorship, artiste, theme
    # staticmethod de création

class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    # description optionnelle du thème ?
    # relation vers authorship, nomination
    # staticmethod de création

class Galerie(db.Model):
    __tablename__ = "galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    # relations vers represente, localisation, authorship
    # staticmethod de création

class Ville(db.Model):
    __tablename__ = "ville"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    # relation vers authorships et localisation
    # staticmethod de création

# tables de relation