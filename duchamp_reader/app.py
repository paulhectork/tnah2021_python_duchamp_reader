from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from .constantes import SECRET_KEY

actual_path = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(actual_path, "templates")
statics = os.path.join(actual_path, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# configurer le secret
app.config['SECRET_KEY'] = SECRET_KEY
# configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
# On initie l'extension
db = SQLAlchemy(app)

# configurer la gestion d'utilisateur-rice-s
login = LoginManager(app)


