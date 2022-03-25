import os
import json
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDFXML
import requests as r

from .regex import clean_string, newline
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
    FILTER (langMatches(lang(?colllabel), "EN"))
  }"""
        if img is not None:
            selectimg = "?img"
            queryimg = """
  # récupérer les urls des images liées à l'artiste
  OPTIONAL {
    wd:{?img} wdt:P18 ?img
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
        try:
            endpoint.setQuery(query)
            if export == "RDFXML":
                if endpoint.supportsReturnFormat(RDFXML):
                    endpoint.setReturnFormat(RDFXML)
                    results = endpoint.query()
                    results_conv = results.convert()
                    with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_out.rdf"), mode="w") as f:
                        f.write(results_conv.toprettyxml())
            elif export == "XML":
                if endpoint.supportsReturnFormat(XML):
                    endpoint.setReturnFormat(XML)
                    results = endpoint.query()
                    results_conv = results.convert()
                    with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_out.xml"), mode="w") as f:
                        f.write(results_conv.toprettyxml())
            else:
                # le format d'export par défaut: JSON (ça marche toujours sur wikidata)
                endpoint.setReturnFormat(JSON)
                results = endpoint.query()
                results_conv = results.convert()
                with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_out.json"), mode="w") as f:
                    json.dump(results_conv, f)

            # enregistrer la requête dans le dossier uploads
            with open(os.path.join(uploads, f"sparql_{nom}_{id_wikidata}_requete.sparql"), mode="w") as f:
                f.write(query)

        except Exception as error:
            url = results.geturl()
            print(url)
            req = r.get(url)
            if req.status_code == 403:
                err.append("L'accès au SPARQL endpoint a été interdit par Wikidata. Si vous avez accès au code source \
                de l'application, modifiez le paramètre 'agent' du SPARQLWrapper() dans le présent fichier, en \
                définissant un agent correspondant à la 'User-Agent Policy' : \
                https://meta.wikimedia.org/wiki/User-Agent_policy.")
            else:
                err.append(error)

    else:
        err.append("L'identifiant wikidata ou le format d'export n'ont pas été fournis.")

    # enregistrer la requête et permettre le DL par l'utilisateurice -- À FAIRE MTN