from warnings import warn
import os

actual_path = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(actual_path, "templates")
statics = os.path.join(actual_path, "static")

SECRET_KEY = "clé secrète par défaut mais franchement faudrait la changer par les temps qui courent"

if SECRET_KEY == "clé secrète par défaut mais franchement faudrait la changer":
    warn("Pour des raisons de sécurité, veuillez changer le secret par défaut", Warning)