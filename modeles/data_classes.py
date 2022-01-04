from flask import url_for
import datetime

from .. import db #importer la base de données du duchamp_reader, que je dois encore créer
# from users.py import User #on importe la classe user / ou alors ptet qu'on devra seult importer une partie
# ou alors rien du tout jsp

# les tables de relation : Authorship(User-autres tables), Represente(Artiste-Galerie), Localisation(Galerie-Ville)
class Authorship(db.Model):
    __tablename__ = "authorship"
    id = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    artiste_id = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    nomination_id = db.Column(db.Integer, db.ForeignKey("nomination.id"))
    galerie_id = db.Column(db.Integer, db.ForeignKey("galerie.id"))
    ville_id = db.Column(db.Integer, db.ForeignKey("ville.id"))
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id"))

    user = db.relationship("User", back_populates="authorships")
    artiste = db.relationship("Artiste", back_populates="authorships")
    nomination = db.relationship("Nomination", back_populates="authorships")
    galerie = db.relationship("Galerie", back_populates="authorships")
    ville = db.relationship("Ville", back_populates="authorships")
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
    date_naissance = db.Column(db.Integer, nullable=False) # format YYYY - à rendre obligatoire dans la fonction de création de nv artistes avec des 'if...not'
    genre = db.Column(db.String(1)) # 3 caractères possibles à entrer dans les fonctions de création : A, F, M
    id_ville_naissance = db.Column(db.Integer, db.ForeignKey("ville.id"))
    id_ville_residence = db.Column(db.Integer, db.ForeignKey("ville.id"))
    id_nomination = db.Column(db.Integer, db.ForeignKey("nomination.id")) # est-ce qu'il doit y avoir une foreignKey ici ? dans l'exemple non
    # +globalement, est-ce que ça peut fausser la construction des tables d'avoir des clés externes vers les tables avec lesquelles on fait le lien, alors qu'il n'y a pas ces clés externes dans la doc

    authorships = db.relationship("User", secondary=Authorship, back_populates="artiste")
    represents = db.relationship("Galerie", secondary=Represente, back_populates="artiste")
    ville_naissance = db.relationship("Ville", foreign_keys=[id_ville_naissance])
    ville_residence = db.relationship("Ville", foreign_keys=[id_ville_residence])
    nomination = db.relationship("Nomination", back_populates="artiste", uselist=False)
    # relation avec Ville du côté de Ville



class Nomination(db.Model):
    __tablename__ = "nomination"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    laureat = db.Column(db.Boolean, nullable=False)
    id_artiste = db.Column(db.Integer, db.ForeignKey("artiste.id"))

    authorships = db.relationship("User", secondary=Authorship, back_populates="nomination")
    artiste = db.relationship("Artiste", back_populates="nomination")
    theme = db.relationship("Theme", back_populates="nominations")
    # staticmethod de création



class Galerie(db.Model):
    __tablename__ = "galerie"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)

    authorships = db.relationship("User", secondary=Authorship, back_populates="galerie")
    represents = db.relationship("Artiste", secondary=Represente, back_populates="galerie")
    localisations = db.relationship("Ville", secondary=Localisation, back_populates="galerie")
    # staticmethod de création



class Ville(db.Model):
    __tablename__ = "ville"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=True) # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste
    latitude = db.Column(db.Float, nullable=True) # je mets nullable=True pour que ça fonctionne avec l'ajout d'artiste

    authorships = db.relationship("User", secondary=Authorship, back_populates="ville")
    localisations = db.relationship("Galerie", secondary=Localisation, back_populates="ville")
    # quoi faire ici pour mettre en relation avec Artiste ?
    # staticmethod de création



class Theme(db.Model):
    __tablename__ = "theme"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)

    authorships = db.relationship("User", secondary=Authorship, back_populates="theme")
    nominations = db.relationship("Nomination", back_populates="theme")
    # colonne de description optionnelle du thème ?
    # staticmethod de création



# les relations dont je suis assez sûr : toutes les tables de relation, la relation artiste-nomination, la relation artiste-theme
# là où j'ai un plus gros doute : les relations artiste-ville, si on doit utiliser ou non Artiste.id_nomination
# je ne suis pas non plus sûr de la manière dont on écrit la valeur de "secondary="
# ni de si, en mettant la table de relation comme relation secondaire (avec "secondary=", il faut, dans la table de relation, faire des db.relationship vers les autres tables ?
# dans les exemples de la doc, avec "secondary=", il n'y a pas de "db.relationship" dans la table de relation, seult des clés externes "ForeignKey"