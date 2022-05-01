import matplotlib.pyplot as plt

from ..modeles.classes_generic import *
from ..modeles.classes_relationships import RelationRepresente, RelationLocalisation

def a_voir(xaxis, yaxis, graph=None):

    # si l'année de nomination est en ordonnées, construire une liste des années
    if xaxis == "annee_nomination":
        maxyear = Nomination.query.order_by(Nomination.annee.desc()).first()
        minyear = Nomination.query.order_by(Nomination.annee.asc()).first()
        print(maxyear.annee, minyear.annee)
        x = list(range(int(minyear.annee), int(maxyear.annee)+1))
        print(x)

    # nombre de thèmes par an
    if yaxis == "theme_count":
        themedict = {}  # dictionnaire associant à chaque thème le nombre d'occurences par an
        theme = Theme.query.all()
        annees = Nomination.query.group_by(Nomination.annee).all()
        for a in annees:
            par_an = Nomination.query.filter(Nomination.annee == a.annee).all()
            for p in par_an:
                print(p)
            """print("###############")
            themedict[t.nom] = Nomination.query.filter(
                Nomination.theme == t).count()"""
        print(themedict)


    # un violon prend:
    # dataset: les données en entrée
    # positions: les positions des violons (années, dans mon cas)
    # vert: créer un violon vertical ou horizontal
    # widths: largeur maximale de chaque violon
