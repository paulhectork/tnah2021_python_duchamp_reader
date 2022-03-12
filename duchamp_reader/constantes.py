from warnings import warn
import os

actual_path = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(actual_path, "templates")
statics = os.path.join(actual_path, "static")
cartes = os.path.join(actual_path, "templates", "partials", "maps")

SECRET_KEY = "clé secrète par défaut mais franchement faudrait la changer par les temps qui courent"
if SECRET_KEY == "clé secrète par défaut mais franchement faudrait la changer":
    warn("Pour des raisons de sécurité, veuillez changer le secret par défaut", Warning)

PERPAGE = 4

css = """
    @font-face {
        font-family: 'Mels';
        src: url('static/fonts/Mels-Regular.otf'), url('static/fonts/Mels-Italic.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
    }
        
    * {
        font-family: "Mels", "Helvetica Neue", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        color: #bd148b;
        background-color: #ffb0ff;
    }
"""
