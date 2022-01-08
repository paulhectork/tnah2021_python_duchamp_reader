from warnings import warn

SECRET_KEY = "clé secrète par défaut mais franchement faudrait la changer par les temps qui courent"

if SECRET_KEY == "clé secrète par défaut mais franchement faudrait la changer":
    warn("Pour des raisons de sécurité, veuillez changer le secret par défaut", Warning)