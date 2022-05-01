from ..modeles.classes_generic import *
from ..app import app

# ce fichier de variables constantes contient toutes les requêtes nécessaires à la sidebar (joli franglais)
# il permet d'éviter les imports circulaires


def queries():
        """
        Fonction lançant des requêtes pour peupler le sidebar avec les derières données
        :return: listes contenant les 3 derniers objets de chaque classe qui ont été ajoutés
        """
        # requêtes
        last_artistes = Artiste.query.order_by(Artiste.id.desc()).limit(3).all()
        last_nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id)\
                .order_by(Nomination.id.desc()).limit(3).all()
        last_galeries = Galerie.query.order_by(Galerie.id.desc()).limit(3).all()
        last_villes = Ville.query.order_by(Ville.id.desc()).limit(3).all()
        last_themes = Theme.query.order_by(Theme.id.desc()).limit(3).all()

        # return
        return last_artistes, last_nominations, last_galeries, last_villes, last_themes

