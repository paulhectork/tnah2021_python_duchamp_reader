from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import atexit, os, glob

from .constantes import SECRET_KEY, templates, statics, cartes

# ----- CONFIGURATION DE L'APPLICATION ----- #
app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# configurer le secret
app.config['SECRET_KEY'] = SECRET_KEY
# configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"check_same_thread": False}
# initier l'extension de la bdd
db = SQLAlchemy(app)
# configurer la gestion d'utilisateur-rice-s
login = LoginManager(app)


# ----- PEUPLER LA BDD ET CONFIGURER L'INDEX ----- #
# vérifier si la bdd est déjà créé ; sinon, la créer et peupler
from .populate import *
db_create()
db_populate()


# ----- NETTOYER LES CARTES ----- #
def nettoyage():
    """Fonction permettant de supprimer les cartes créées pendant l'utilisation et stockées dans le dossier "maps/".
    Cela permet d'éviter la coexistence de différentes versions de cartes (la manière dont les cartes sont créées a
    évolué avec le temps; il faut mieux tout supprimer et recréer à chaque utilisation).

    :return: dossier "maps/" vidé de tous ses contenus
    :rtype: None
    """
    a_suppr = glob.glob(os.path.join(cartes, "*.html"))
    try:
        for f in a_suppr:
            os.remove(f)
    except Exception as erreur:
        print(erreur)
        return False, [str(erreur)]


atexit.register(nettoyage)


# ----- EVITER LES IMPORTS CIRCULAIRES ET AUTRES ----- #
from .routes import *  # importer les routes utilisées par l'application

