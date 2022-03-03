from sqlalchemy_utils.functions import database_exists

from .app import db
from .modeles import classes_users, classes_generic
# j'ai dû faire classes_users ça sinon j'avais une erreur:
# Missing user_loader or request_loader

def db_create():
    if not database_exists('sqlite:///db.sqlite'):
        db.create_all()

def db_populate():
    if not Artiste.query.get(1):
        Artiste.artiste_new_init("Fontaine", "Claire", 1985, "F", 1, 1)
