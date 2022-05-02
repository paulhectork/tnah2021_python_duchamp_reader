import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
from scipy.interpolate import interp1d
from io import BytesIO
import numpy as np
import base64

from ..modeles.classes_generic import *
from ..modeles.classes_relationships import RelationRepresente


def a_voir(axis, graph):
    """
    fonction permettant de construire une visualisation avec matplotlib (malheureusement,
    plotly a été découvert trop tard pour l'utiliser, alors que cette librairie permet
    de générer des fichiers HTML). lorsque le formulaire est envoyé, des requêtes sqlalchemy
    sont construites ; le résultat est stocké dans un dictionnaire pour ensuite construire
    un graphique
    :param axis: les données à traiter
    :param graph: le type de graphe à produire
    :return: si tout va bien, un URL permettant de passer le graphique à Flask puis à Jinja
    et un message d'erreur vide; sinon, un message d'erreur et un URL vide
    """

    # PRÉPARATION DES DONNÉES
    # vérifier que les données ont été fournies
    erreurs = []
    if axis == "None":
        erreurs.append("Veuillez indiquer les données à traiter")
    if graph == "None":
        erreurs.append("Veuillez indiquer le type de graphique à produire")

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

        # CONSTRUCTION DU GRAPHIQUE
        dummy = BytesIO()  # construire un objet IO à passer à Flask puis Jinja
        fig, ax = plt.subplots()

        # définir le style: police, feuille de style
        plt.rcParams.update(plt.rcParamsDefault)
        fontdir = "../static/fonts"
        for f in fm.findSystemFonts(fontpaths=fontdir, fontext="otf"):
            fm.fontManager.addfont(f)
        rcParams["font.family"] = "Mels"
        plt.style.use("dark_background")

        # génération des graphiques
        if axis == "theme_count":
            if graph == "bar":
                ax = bar(input_dict=themedict, input_ax=ax, input_x=x)
            elif graph == "scatter":
                ax = scatter(input_dict=themedict, input_ax=ax, input_x=x)
            else:
                plotter(input_dict=themedict, input_x=x)
            ax.set_title("Nombre de thèmes par an")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de thèmes")

        if axis == "galerie_count":
            if graph == "bar":
                ax = bar(input_dict=galdict, input_ax=ax, input_x=x)
            elif graph == "scatter":
                ax = scatter(input_dict=galdict, input_ax=ax, input_x=x, galflag=True)
            else:
                plotter(input_dict=galdict, input_x=x, galflag=True)
            ax.set_title("Nombre de galeries représentant des nominé.e.s par an")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de galeries")

        if axis == "pays_count":
            # si c'est un graphique en barres, construire le graphique en barres
            if graph == "bar":
                ax = bar(input_dict=paysdict, input_ax=ax, input_x=x)
            elif graph == "scatter":
                ax = scatter(input_dict=paysdict, input_ax=ax, input_x=x)
            else:
                plotter(input_dict=paysdict, input_x=x)
            ax.set_title("Nombre de nominé.e.s par pays et par an")
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de nominé.e.s nés ou habitant dans un pays")

        # finalisation du graphique, génération d'un URL à partir duquel intégrer le graphique sur la page
        # html et sauvegarde du dummy
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.savefig(dummy, format="png", bbox_inches="tight")
        plt.close()
        dummy.seek(0)
        url = base64.b64encode(dummy.getvalue()).decode('utf8')

    # return
    return url, erreurs


def plotter(input_dict, input_x, galflag=False):
    """
    construire un graphique en courbes où les courbes subissent une interpolation
    quadratique pour être arrondies. deux comportements différents sont possibles:
        - pour les thèmes et les pays, les données sont affichées pour chaque thème/pays,
          comme dans les graphiques en barres
        - pour les galeries, c'est la somme des galeries qui est montrée
    la fonction construit également l'annotation de chaque courbe
    :param input_dict: dictionnaire à partir duquel construire le graphique
    :param input_x: axe des abscisses
    :param galflag: flag indiquant si il s'agit des galeries (et qu'il faut faire la somme des données) ou non
    :return: None
    """
    if not galflag:
        for k, v in input_dict.items():
            model = interp1d(input_x, v, kind="quadratic")
            np_x = np.array(input_x)
            xaxis = np.linspace(np_x.min(), np_x.max())
            yaxis = model(xaxis)
            plt.plot(xaxis, yaxis, label=k)
            # annotation des courbes en nettoyant le texte produit
            annot(input_x=input_x, input_y=v)
    else:
        vsum = np.zeros(len(input_x))
        for v in input_dict.values():
            vsum = vsum + v
        annot(input_x=input_x, input_y=vsum)
        model = interp1d(input_x, vsum, kind="quadratic")
        np_x = np.array(input_x)
        xaxis = np.linspace(np_x.min(), np_x.max())
        yaxis = model(xaxis)
        plt.plot(xaxis, yaxis, label="Nombre de galeries représentées par an")
    return None


def bar(input_dict, input_x, input_ax):
    """
    construire un graphique en barres avec des annotations. chaque entrée du dictionnaire est
    empilée au dessus des autres grâce à une variable "bottom" incrémentée à chaque itération
    sur le dictionnaire
    :param input_dict: dictionnaire à partir duquel construire les graphiques
    :param input_x: axe des abscisses
    :param input_ax: objet ax du graphique en cours de création
    :return: objet ax stockant les différentes courbes
    """
    bottom = np.zeros(len(list(input_dict.values())[0]))  # pour construire l'offset vertical et empiler les ax.bar
    for k, v in input_dict.items():
        input_ax.bar(x=input_x, height=v, width=0.4, bottom=bottom, label=k)
        bottom = bottom + v
    return input_ax


def scatter(input_dict, input_x, input_ax, galflag=False):
    """
    fonction permettant la création et l'annotation d'un graphique en nuages de points. pour les galeries,
    le comportement est différent: c'est la somme des galeries qui représentent un.e artiste par an qui
    est représentée
    :param input_dict: dictionnaire pour la création du graphique
    :param input_x: axe des abscisses
    :param input_ax: objet ax du graphique en cours de création
    :param galflag: un flag permettant d'indiquer si on travaille sur les galeries pour calculer la somme
    :return: objet ax stockant les différentes courbes
    """
    if galflag is False:
        for k, v in input_dict.items():
            input_ax.scatter(x=input_x, y=v, label=k)
            annot(input_x=input_x, input_y=v)
    else:
        vsum = np.zeros(len(input_x))
        for k, v in input_dict.items():
            vsum = vsum + v
            input_ax.scatter(x=input_x, y=vsum, label=k)
            annot(input_x=input_x, input_y=vsum)
    return input_ax


def annot(input_x, input_y):
    """
    fonction permettant l'annotation des graphiques en nuages de points et
    des graphiques à courbes
    :param input_x: axe des abscisses à annoter
    :param input_y: axe des ordonnées à annoter
    :return: None
    """
    for xzip, yzip in zip(input_x, input_y):
        ann = re.sub(r"\(", "", str(yzip))
        ann = re.sub(r"\)", "", ann)
        ann = re.sub(r":", "", ann)
        plt.annotate(ann, (xzip, yzip),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha="center")
    return None
