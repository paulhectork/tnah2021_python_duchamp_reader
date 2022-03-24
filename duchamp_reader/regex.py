import re

regexwkd = "^Q\d+$" # regex vérifiant les ID wikidata
regexnp = "^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$" # l'expression régulière utilisée pour vérifier la validité des noms propres : majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne
regexnc = "^(([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])|(\-?\s?))+([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+$" # l'expression régulière pour vérifier la validité des noms communs : caractères en minuscules, accentués ou non, séparés ou non par un unique espace ou tiret
regexmail = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" # l'expression régulière pour vérifier la validité des mails; source: https://www.emailregex.com/
regexurl = "http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"  # expression régulière
# validant les URL

def clean_string(chaine):
    """Fonction pour nettoyer une chaîne de caractères à l'aide d'expressions régulières :
    séparer les mots par un seul espace ou tiret, supprimer les espaces en début et fin de chaîne

    :param chaine: la chaîne de caractères à nettoyer
    :type chaine: str
    :return: la chaîne nettoyée (espaces normalisés,
    :rtype: str
    """
    chaine = str(chaine) # pour être sûr de ne pas se taper des mauvais messages d'erreurs
    chaine = re.sub("\s{2,}", " ", chaine)
    chaine = re.sub("-{2,}", "-", chaine)
    chaine = chaine.strip()
    return chaine