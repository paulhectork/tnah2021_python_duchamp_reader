from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from populate import *

from .constantes import SECRET_KEY, templates, statics

# actual_path = os.path.dirname(os.path.abspath(__file__))
# templates = os.path.join(actual_path, "templates")
# statics = os.path.join(actual_path, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# configurer le secret
app.config['SECRET_KEY'] = SECRET_KEY
# configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# On initie l'extension
db = SQLAlchemy(app)

# configurer la gestion d'utilisateur-rice-s
login = LoginManager(app)

# éviter les imports circulaires
from .routes import * # importer les routes utilisées par l'application

# vérifier si la bdd est déjà créé ; sinon, la créer et peupler
db_create()
db_populate()
