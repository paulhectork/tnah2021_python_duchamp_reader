from ..modeles.classes_generic import *

# ce second fichier de variables constantes contient toutes les requêtes nécessaires à la sidebar (joli franglais)
# il permet d'éviter les imports circulaires
last_artistes = Artiste.query.order_by(Artiste.id.desc()).limit(3).all()
last_nominations = Nomination.query.join(Artiste, Nomination.id_artiste == Artiste.id)\
        .order_by(Nomination.id.desc()).limit(3).all()
last_galeries = Galerie.query.order_by(Galerie.id.desc()).limit(3).all()
last_villes = Ville.query.order_by(Ville.id.desc()).limit(3).all()
last_themes = Theme.query.order_by(Theme.id.desc()).limit(3).all()
