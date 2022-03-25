import wikipedia
from wikipedia import WikipediaException, DisambiguationError

def wikimaker(full, nom):
    # définition des variables qui serviront à affichier les informations de wikipedia
    wikidict = {}  # dictionnaire associant à un titre de page une url, pour afficher des pages au hasard si erreur
    wikipage = None
    url = ""
    travail = ""
    oeuvre = ""
    summary = ""
    bio = ""
    formation = ""
    carriere = ""
    oe = "\u0152"
    # commencer par chercher la page wikipedia en français; si elle existe, récupérer des sections
    try:
        wikipedia.set_lang("fr")
        wikipage = wikipedia.page(full, auto_suggest=True)
        if nom in wikipage.title:
            summary = wikipage.summary
            url = wikipage.url
            if wikipage.section("Biographie"):
                bio = wikipage.section("Biographie")
            elif wikipage.section("Formation"):
                formation = wikipage.section("Formation")
            elif wikipage.section("Carrière"):
                carriere = wikipage.section("Carrière")
            elif wikipage.section("Travail"):
                travail = wikipage.section("Travail")
            elif wikipage.section(f"{oe}uvre"):
                oeuvre = wikipage.section(f"{oe}uvre")
            elif wikipage.section(f"{oe}uvres"):
                oeuvre = wikipage.section(f"{oe}uvres")
            code = "fr"  # code pour savoir quelles données wikipedia sont affichées
        # si la mauvaise page a été requêtée par erreur, proposer des renvois vers 4 pages au hasard
        else:
            wikipedia.set_lang("fr")
            wikilist = wikipedia.random(pages=4)  # 4 pages au hasard si on ne trouve pas de page pour l'artiste
            for w in wikilist:
                try:
                    wikidict[w] = wikipedia.page(w).url
                except DisambiguationError as e:
                    try:
                        wikidict[e.options[0]] = wikipedia.page(e.options[0].url)
                    except WikipediaException:
                        wikidict[e.options[0]] = None
            code = "no"

    # si la page n'existe pas en français, la chercher en anglais
    except WikipediaException:
        try:
            wikipedia.set_lang("en")
            wikipage = wikipedia.page(full, auto_suggest=True)
            if nom in wikipage.title:
                summary = wikipage.summary
                url = wikipage.url
                if wikipage.section("Biography"):
                    bio = wikipage.section("Biography")
                elif wikipage.section("Life and work"):
                    bio = wikipage.section("Life and work")
                elif wikipage.section("Early life"):
                    formation = wikipage.section("Early life")
                elif wikipage.section("Education"):
                    formation = wikipage.section("Education")
                elif wikipage.section("Early life and education"):
                    formation = wikipage.section("Early life and education")
                elif wikipage.section("Career"):
                    carriere = wikipage.section("Career")
                elif wikipage.section("Work"):
                    travail = wikipage.section("Work")
                elif wikipage.section("Artistic practice"):
                    oeuvre = wikipage.section("Artistic practice")
                elif wikipage.section("Art"):
                    oeuvre = wikipage.section("Art")
                code = "en"
            # si la mauvaise page a été requêtée par erreur, proposer des renvois vers 4 pages au hasard
            else:
                wikipedia.set_lang("fr")
                wikilist = wikipedia.random(pages=4)  # 4 pages au hasard si on ne trouve pas de page pour l'artiste
                for w in wikilist:
                    try:
                        wikidict[w] = wikipedia.page(w).url
                    except DisambiguationError as e:
                        try:
                            wikidict[e.options[0]] = wikipedia.page(e.options[0].url)
                        except WikipediaException:
                            wikidict[e.options[0]] = None
                code = "no"

        # si la page n'est trouvée ni en français, ni en anglais, proposer une liste de 4 pages au hasard
        except WikipediaException:
            wikipedia.set_lang("fr")
            wikilist = wikipedia.random(pages=4)  # 4 pages au hasard si on ne trouve pas de page pour l'artiste
            for w in wikilist:
                try:
                    wikidict[w] = wikipedia.page(w).url
                except DisambiguationError as e:
                    try:
                        wikidict[e.options[0]] = wikipedia.page(e.options[0].url)
                    except Exception:
                        # si rien ne marche, créer une entrée vide dans le dictionnaire
                        wikidict[None] = None
            code = "no"

    # return
    return code, summary, bio, formation, carriere, travail, oeuvre, url, wikidict
