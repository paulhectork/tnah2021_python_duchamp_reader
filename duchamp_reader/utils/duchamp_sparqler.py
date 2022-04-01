import os
import json
import requests as r
from datetime import datetime, timezone, timedelta
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDFXML

from .regex import clean_string, clean_time, newline
from .constantes import uploads


def duchamp_sparqler(nom, id_wikidata, url, collection, img, id_isni,
                     id_viaf, id_bnf, id_congress, id_artsy, export):
    """Fonction permettant de construire des requêtes Wikidata sur des artistes à l'aide d'un formulaire.
    Les requêtes sont enregistrées au format choisi par l'utilisateurice (RDFXML, XML ou JSON). L'indentation
    des bouts de requête n'est pas très élégante mais ça permet de sortir la plus jolie feuille sparql possible.

    :param nom:
    :param id_wikidata:
    :param url:
    :param collection:
    :param img:
    :param id_isni:
    :param id_viaf:
    :param id_bnf:
    :param id_congress:
    :param id_artsy:
    :param export:
    :return:
    """
    err = []  # liste vide pour stocker les erreurs
    if id_wikidata is not None and export is not None:
        now = clean_time(datetime.now(timezone(timedelta(hours=+1))).isoformat())  # l'heure actuelle
        datadict = {}  # dictionnaire associant varlist a datalist pour afficher les résultats d'une requête en html
        # moduler les requêtes et les variables à inclure dans le SELECT
        queryurl = ""
        querycoll = ""
        queryimg = ""
        queryisni = ""
        queryviaf = ""
        querybnf = ""
        querycongress = ""
        queryartsy = ""
        queryend = "}"
        selecturl = ""
        selectcoll = ""
        selectimg = ""
        selectisni = ""
        selectviaf = ""
        selectbnf = ""
        selectcongress = ""
        selectartsy = ""
        queryprefix = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX schema: <http://schema.org/>"""  # liste des préfixes pour la requête
        querybase = """
WHERE {

  # retourner l'id wikidata de la personne sur qui la requête est faite
  VALUES ?id {"{ID}"}

  # récupérer le nom de la personne sur qui la requête est faite
  OPTIONAL {
    wd:{ID} rdfs:label ?labelen .
    FILTER (langMatches(lang(?labelen), "EN"))
  }"""  # l'ID et le label de l'artiste seront toujours demandés
        if url is not None:
            selecturl = "?url"
            queryurl = """
  # récupérer son site web officiel, si il existe
  OPTIONAL {
    wd:{ID} wdt:P856 ?url
  }"""
        if collection is not None:
            selectcoll = "?collid ?colllabel"
            querycoll = """
  # récupérer les id et les noms des collections possédant des oeuvres de l'artiste
  OPTIONAL {
    wd:{ID} wdt:P6379 ?collid .
    ?collid rdfs:label ?colllabel .
    FILTER (langMatches(lang(?colllabel), "EN-GB"))
  }"""
        if img is not None:
            selectimg = "?img"
            queryimg = """
  # récupérer les urls des images liées à l'artiste
  OPTIONAL {
    wd:{ID} wdt:P18 ?img
  }"""
        if id_isni is not None:
            selectisni = "?idisni"
            queryisni = """
  # récupérer son identifiant ISNI, si il existe
  OPTIONAL {
      wd:{ID} wdt:P213 ?idisni
  }"""
        if id_viaf is not None:
            selectviaf = "?idviaf"
            queryviaf = """
  # récupérer son identifiant VIAF, si il existe
  OPTIONAL {
    wd:{ID} wdt:P214 ?idviaf
  }"""
        if id_bnf is not None:
            selectbnf = "?idbnf"
            querybnf = """
  # récupérer son identifiant BNF, si il existe
  OPTIONAL {
    wd:{ID} wdt:P268 ?idbnf
  }"""
        if id_congress is not None:
            selectcongress = "?idcongress"
            querycongress = """
  # récupérer son identifiant à la Library of Congress, si il existe
  OPTIONAL {
    wd:{ID} wdt:P244 ?idcongress
  }"""
        if id_artsy is not None:
            selectartsy = "?idartsy"
            queryartsy = """
  # récupérer son identifiant Artsy, si il existe
  OPTIONAL {
    wd:{ID} wdt:P2042 ?idartsy
  }"""

        # construire le select et la requête
        queryselect = f"SELECT ?id ?labelen {selecturl} {selectcoll} {selectimg} {selectisni} {selectviaf} {selectbnf} \
{selectcongress} {selectartsy}"
        queryselect = clean_string(queryselect)
        query = f"""{queryprefix}
{queryselect}
{querybase}
{queryurl}
{querycoll}
{queryimg}
{queryisni}
{queryviaf}
{querybnf}
{querycongress}
{queryartsy}
{queryend}
""".replace("{ID}", id_wikidata)
        query = newline(query)

        # lancer la requête sparql
        endpoint = SPARQLWrapper("https://query.wikidata.org/sparql",
                                 agent="MarcelDuchampBot/1.0 \
                                       (http://127.0.0.1:5000/sparql; marcel_duchamp@duchampreader.com) \
                                       Flask/2.0.2")

        # lancer la requête au format demandé par l'utilisateurice si ce format existe. enregistrer le résultat
        # de la requête au bon format, ainsi que la requête
        try:
            endpoint.setQuery(query)
            if export == "RDFXML":
                if endpoint.supportsReturnFormat(RDFXML):
                    endpoint.setReturnFormat(RDFXML)
                    results = endpoint.query()
                    results_conv = results.convert()
                    with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_{now}_out.rdf"), mode="w") as f:
                        f.write(results_conv.toprettyxml())
                    outname = f"sparql_{nom}_{id_wikidata}_{now}_out.rdf"

            elif export == "XML":
                if endpoint.supportsReturnFormat(XML):
                    endpoint.setReturnFormat(XML)
                    results = endpoint.query()
                    results_conv = results.convert()
                    with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_{now}_out.xml"), mode="w") as f:
                        f.write(results_conv.toprettyxml())
                    outname = f"sparql_{nom}_{id_wikidata}_{now}_out.xml"
            else:
                # le format d'export par défaut: JSON (ça marche toujours sur wikidata)
                endpoint.setReturnFormat(JSON)
                results = endpoint.query()
                results_conv = results.convert()
                with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_{now}_out.json"), mode="w") as f:
                    json.dump(results_conv, f)
                outname = f"sparql_{nom}_{id_wikidata}_{now}_out.json"

            # enregistrer la requête dans le dossier uploads
            with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_{now}_query.sparql"), mode="w") as f:
                f.write(query)
            queryname = f"sparql_{nom}_{id_wikidata}_{now}_query.sparql"

        # en cas d'erreur, retourner un message d'erreur. si wikidata renvoie un code 403 (Forbidden), c'est
        # probablement un problème d'User-Agent
        except Exception as error:
            url = results.geturl()
            req = r.get(url)
            if req.status_code == 403:
                err.append("L'accès au SPARQL endpoint a été interdit par Wikidata. Si vous avez accès au code source \
                de l'application, modifiez le paramètre 'agent' du SPARQLWrapper() dans le présent fichier, en \
                définissant un agent correspondant à la 'User-Agent Policy' : \
                https://meta.wikimedia.org/wiki/User-Agent_policy.")
            else:
                err.append(error)
            return err

        # construire un dictionnaire à partir d'une requête json pour afficher les résultats de la requête en HTML
        if export != "JSON":
            endpoint.setReturnFormat(JSON)
            results_json = endpoint.query()
            results_json = results_json.convert()
        else:
            results_json = results_conv
        datalist = results_json["results"]["bindings"]
        # itérer sur le JSON pour créer un dictionnaire qui associe à chaque variable recherchée la liste des résultats
        for d in datalist:
            for k, v in d.items():
                try:
                    if k not in datadict.keys():
                        datadict[k] = v["value"]
                    else:
                        datadict[k] += f", {v['value']}"
                except Exception:
                    datadict[k] = "information non disponible"

    else:
        err.append("L'identifiant wikidata ou le format d'export n'ont pas été fournis.")

    return outname, queryname, err, datadict
