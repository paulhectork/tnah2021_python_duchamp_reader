import datetime

from .. import db

# les tables de relation : tables d'Authorship, Represente(Artiste-Galerie), Localisation(Galerie-Ville)
class Authorship_Artiste(db.Model):
    __tablename__ = "authorship_artiste"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    user = db.relationship("User", back_populates="authorships")
    artiste = db.relationship("Artiste", back_populates="authorships")


class Authorship_Nomination(db.Model):
    __tablename__ = "authorship_nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_nomination = db.Column(db.Integer, db.ForeignKey("nomination.id"))
    user = db.relationship("User", back_populates="authorships")
    nomination = db.relationship("Nomination", back_populates="authorships")


class Authorship_Galerie(db.Model):
    __tablename__ = "authorship_galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_galerie = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    user = db.relationship("User", back_populates="authorships")
    galerie = db.relationship("Galerie", back_populates="authorships")


class Authorship_Ville(db.Model):
    __tablename__ = "authorship_ville"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_ville = db.Column(db.Integer, db.ForeignKey("ville.id"))
    user = db.relationship("User", back_populates="authorships")
    ville = db.relationship("Ville", back_populates="authorships")


class Authorship_Theme(db.Model):
    __tablename__ = "authorship_theme"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_theme = db.Column(db.Integer, db.ForeignKey("theme.id"))
    user = db.relationship("User", back_populates="authorships")
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
    date_naissance = db.Column(db.Integer, nullable=False) #format YYYY
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
    # à ajouter : staticmethod de création de données


class Nomination(db.Model):
    __tablename__ = "nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    date = db.Column(db.Integer, nullable=False) # format YYYY
    laureat = db.Column(db.Boolean, nullable=False) # 1 si lauréat, 0 si non
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))

    authorships = db.relationship("Authorship_Nomination", back_populates="nomination")
    artiste = db.relationship("Artiste", back_populates="nomination")
    theme = db.relationship("Theme", back_populates="nominations", uselist = False)
    # staticmethod de création de données


class Galerie(db.Model):
    __tablename__ = "galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)

    authorships = db.relationship("Authorship_Galerie", back_populates="galerie")
    represents = db.relationship("Represente", back_populates="galerie")
    localisations = db.relationship("Localisation", back_populates="galerie")
    # staticmethod de création de données


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
    # staticmethod de création de données


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
