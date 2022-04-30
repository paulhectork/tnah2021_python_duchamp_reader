from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import atexit, os, glob

from .utils.constantes import SECRET_KEY, templates, statics, cartes, uploads

# ----- CONFIGURATION DE L'APPLICATION ----- #
app = Flask(
    "Duchamp Reader",
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
from .utils.populate import db_create, db_populate
db_create()
db_populate()


# ----- NETTOYER LES FICHIERS CRÉÉS PENDANT L'UTILISATION ----- #
def nettoyage():
    """Fonction permettant de supprimer les fichiers créées pendant l'utilisation et stockées dans les dossiers
    "templates/partials/maps" et "templates/upload. Cela permet d'éviter de surcharger la mémoire de l'ordinateur.
    ATTENTION - cette fonction supprime tous les fichiers à chaque modification des scripts python. Pour un résultat efficace,
    éviter de changer les scripts pendant que l'application est en cours d'utilisation.

    :return: dossier "templates/partials/maps" et "templates/uploads" vidés de leurs contenus
    :rtype: None
    """
    cartes_html = glob.glob(os.path.join(cartes, "*.html"))
    sparql_json = glob.glob(os.path.join(uploads, "*.json"))
    sparql_rdf = glob.glob(os.path.join(uploads, "*.rdf"))
    sparql_xml = glob.glob(os.path.join(uploads, "*.xml"))
    sparql_sparql = glob.glob(os.path.join(uploads, "*.sparql"))
    try:
        for f in cartes_html:
            os.remove(f)
        for f in sparql_json:
            os.remove(f)
        for f in sparql_rdf:
            os.remove(f)
        for f in sparql_xml:
            os.remove(f)
        for f in sparql_sparql:
            os.remove(f)
    except Exception as erreur:
        print(erreur)
        return False, [str(erreur)]


atexit.register(nettoyage)


# ----- EVITER LES IMPORTS CIRCULAIRES ET AUTRES ----- #
from .routes import *  # importer les routes utilisées par l'application

