import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

from ..modeles.classes_generic import *
from ..modeles.classes_relationships import RelationRepresente, RelationLocalisation

def a_voir(axis, graph=None):

    erreurs = []
    if axis == "None":
        erreurs.append("Veuillez indiquer les données à traiter")
    """if graph == "None":
        erreurs.append("Veuillez indiquer le type de graphique à produire")
    """
    if len(erreurs) > 0:
        url = None

    else:
        # construire une liste des années à utiliser en ordonnée
        maxyear = Nomination.query.order_by(Nomination.annee.desc()).first()
        minyear = Nomination.query.order_by(Nomination.annee.asc()).first()
        x = list(range(int(minyear.annee), int(maxyear.annee)+1))

        # nombre de thèmes par an
        if axis == "theme_count":
            themedict = {}  # dictionnaire associant à chaque thème le nombre d'occurences par an
            theme = Theme.query.all()
            for t in theme:
                themedict[t.nom] = []
                for annee in x:
                    par_an = Nomination.query.filter(db.and_(
                        Nomination.theme == t,
                        Nomination.annee == annee)
                    ).count()
                    themedict[t.nom].append(par_an)

        # nombre de galeries par an
        if axis == "galerie_count":
            galdict = {}  # dictionnaire associant à chaque galerie le nombre d'artistes nominés par an
            galerie = Galerie.query.all()
            for g in galerie:
                rlist = []  # pour chaque galerie, liste du nombre d'artistes représentés par an
                for annee in x:
                    nom_par_an = Nomination.query.filter(Nomination.annee == annee).all()
                    art_par_an_id = []  # liste des identifiants des artistes pour une année
                    for n in nom_par_an:
                        art_par_an_id.append(n.id_artiste)

                    r = RelationRepresente.query.filter(db.and_(
                        RelationRepresente.id_artiste.in_(art_par_an_id),
                        RelationRepresente.id_galerie == g.id
                    )).count()  # nombre d'artistes représentés par une galerie par an

                    rlist.append(r)
                galdict[g.nom] = rlist

        # pays d'origine ou de résidence des artistes par an
        if axis == "pays_count":
            paysdict = {}  # dictionnaire associant à chaque pays le nombre de nominés qui y sont nés par an
            pvmap = {}  # dictionnaire associant à chaque pays les identifiants des villes qui s'y trouvent
            villes = Ville.query.all()
            # créer une liste d'identifiants de ville
            for v in villes:
                if v.pays not in list(pvmap.keys()):
                    pvmap[v.pays] = [v.id]
                else:
                    pvmap[v.pays].append(v.id)

            for p in pvmap:
                print(pvmap[p])
                alist = []  # pour chaque pays, liste du nombre d'artistes y vivant chaque année
                for annee in x:
                    nom_par_an = Nomination.query.filter(Nomination.annee == annee).all()
                    art_par_an_id = []  # liste des identifiants des artistes pour une année
                    for n in nom_par_an:
                        art_par_an_id.append(n.id_artiste)

                    a = Artiste.query.filter(db.and_(
                        db.or_(
                            Artiste.id_ville_naissance.in_(pvmap[p]),
                            Artiste.id_ville_residence.in_(pvmap[p])
                        ),
                        Artiste.id.in_(art_par_an_id)
                    )).count()

                    alist.append(a)
                # supprimer les pays où aucun artiste n'est né ou n'habite
                if sum(alist) != 0:
                    paysdict[p] = alist

        # construction du graphique
        dummy = BytesIO()  # construire un objet IO à passer à flask puis Jinja
        fig, ax = plt.subplots()
        plt.style.use("dark_background")

        if axis == "theme_count":
            values = list(themedict.values())
            bottom = np.zeros(len(values[1]))  # pour construire l'offset vertical et empiler les ax.bar
            for k, v in themedict.items():
                ax.bar(x=x, height=v, width=0.4, bottom=bottom, label=k)
                bottom = bottom + v
            ax.set_title("Nombre de thèmes par an")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de thèmes")

        if axis == "galerie_count":
            values = list(galdict.values())
            bottom = np.zeros(len(values[1]))  # pour construire l'offset vertical et empiler les ax.bar
            for k, v in galdict.items():
                ax.bar(x=x, height=v, width=0.4, bottom=bottom, label=k)
                bottom = bottom + v
            ax.set_title("Nombre de galeries représentant un.e nominé.e")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de galeries")

        if axis == "pays_count":
            values = list(paysdict.values())
            bottom = np.zeros(len(values[1]))  # pour construire l'offset vertical et empiler les ax.bar
            for k, v in paysdict.items():
                ax.bar(x=x, height=v, width=0.4, bottom=bottom, label=k)
                bottom = bottom + v
            ax.set_title("Nombre de nominé.e.s par pays et par an")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de nominé.e.s nés ou habitant dans un pays")

        plt.legend(bbox_to_anchor=(1.05, 0.6))
        plt.savefig(dummy, format="png", bbox_inches="tight")
        plt.close()
        dummy.seek(0)
        url = base64.b64encode(dummy.getvalue()).decode('utf8')

    # return
    return url, erreurs
