import re

# regexnp = "^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$" ancienne expression régulière

# l'expression régulière utilisée pour vérifier la validité des noms propres : majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, tirets et espaces, miniscule en fin de chaîne
regexnp = "^[A-Z]([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+([\s\-]([a-z]|['\s])*[A-Z]([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)*$"
# l'expression régulière pour vérifier la validité des noms communs : caractères en minuscules,
# accentués ou non, séparés ou non par un unique espace ou tiret
regexnc = "^(([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])|(\-?\s?))+([a-z]|[àáâäéèêëíìîïòóôöúùûüøœæ])+$"
# l'expression régulière pour vérifier la validité des mails; source: https://www.emailregex.com/
regexmail = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
# expression régulière validant les URL
regexurl = "http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
regexwkd = "^Q\d+$" # regex vérifiant les ID wikidata

def clean_string(chaine):
    """Fonction pour nettoyer une chaîne de caractères à l'aide d'expressions régulières :
    séparer les mots par un seul espace ou tiret, supprimer les espaces en début et fin de chaîne,
    remplacer les majuscules accentuées les plus courantes par des majuscules non-accentuées

    :param chaine: la chaîne de caractères à nettoyer
    :type chaine: str
    :return: la chaîne nettoyée (espaces normalisés,
    :rtype: str
    """
    chaine = str(chaine) # pour être sûr de ne pas se taper des mauvais messages d'erreurs
    chaine = re.sub(r"\s{2,}", " ", chaine)
    chaine = re.sub(r"-{2,}", "-", chaine)
    chaine = re.sub(r"(É|Ë|Ê)", "E", chaine)
    chaine = re.sub(r"(Ä|Â|À)", "A", chaine)
    chaine = re.sub(r"(Ô|Ö|Ò)", "0", chaine)
    chaine = chaine.strip()
    return chaine

def newline(chaine):
    """Fonction pour nettoyer le texte généré automatiquement: remplace plusieurs sauts de ligne
    par un seul saut de ligne.

    :param: chaine: la chaîne de caractères à nettoyer
    :type chaine: str
    :return: la chaîne avec les sauts de lignes normalisés
    :rtype: str
    """
    chaine = re.sub(r"\n{2,}", r"\n\n", chaine)
    return chaine


def clean_time(chaine):
    """Fonction permettant de nettoyer et abréger un objet datetime au format ISO.

    :param chaine: un objet datetime
    :type chaine: str
    :return: objet datetime nettoyé et raccourci
    :rtype: str
    """
    chaine = re.sub(r"\.|:", "-", chaine)# définir l'heure pour nommer les fichiers
    chaine = re.sub(r"-\d{5,}\+01-00", "", chaine)
    return chaine
