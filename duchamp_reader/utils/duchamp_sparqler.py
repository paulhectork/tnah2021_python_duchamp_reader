import os
import json
from SPARQLWrapper import SPARQLWrapper, JSON

queryprefix = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX schema: <http://schema.org/>
"""
querybase = """
SELECT ?id ?labelen ?url
  WHERE {
        
    # retourner l'id wikidata de la personne sur qui la requête est faite
    VALUES ?id {"{ID}"}
          
    # récupérer le nom de la personne sur qui la requête est faite
    OPTIONAL {
      wd:{ID} rdfs:label ?labelen .
      FILTER (langMatches(lang(?labelen), "EN"))
    }
"""  # la ligne SELECT de cette base là devra être modulée en fonction des champs requêtés

queryurl = """
    # récupérer son site web officiel, si il existe
    OPTIONAL {
      wd:{ID} wdt:P856 ?url
    }
"""

queryend = """
}
"""


def duchamp_sparqler(id_wikidata, url, collection, id_isni,
                     id_viaf, id_bnf, id_congress, id_artsy):

    if id_wikidata != "None":
        query = f"{queryprefix}\n{querybase}\n{queryurl}\n{queryend}".replace("{ID}", id_wikidata)
        print(query)

    # construire des templates sparql pour chaque keyword -- EN COURS

    # construire une requête sparql complete -- LA MEILLEURE MÉTHODE SERAIT PEUT-ÊTRE DE CRÉER
    # UN DICTIONNAIRE QUI ASSOCIE À CHAQUE MOT CLÉ LA REQUÊTE QU'IL FAUT, ET ENSUITE DE CONSTRUIRE LA REQUÊTE
    # DU COUP JE RAJOUTE DES "VALUE" À MES CHECKBOX POUR FACILITER LA CONSTRUICTION DU DICO

    # OU ALORS ON FAIT UN FORMAT AVEC DES ELEMENTS NUMERORÉS query = "{1}{2}{3}"...

    # lancer la requête

    # enregistrer la requête