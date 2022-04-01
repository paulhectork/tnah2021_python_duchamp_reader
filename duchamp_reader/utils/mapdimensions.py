def mapdim(longlist, latlist):
    """Fonction permettant de définir en fonction des données à afficher (sous la forme de marqueurs) :
       - les dimensions d'une carte
       - la zone qu'elle couvre et le point sur lequel elle est centrée
       - la taille des marqueurs (des cercles qui affichent une fenête contenant des informations si on clique dessus
    À utiliser sur pour les cartes des pages "Galerie" et "Artiste", qui doivent afficher plusieurs localisations.

    :param longlist: liste des longitudes devant figurer sur la carte
    :type longlist: list
    :param latlist: liste des latitudes devant figurer sur la carte
    :type latlist: list
    :return: variables permettant de générer une carte aux bonnes dimensions
    :return sw: point extrême sud-ouest figurant sur la carte
    :rtype sw: list
    :return ne: point extrême nord-est devant figurer sur la carte
    :rtype ne: list
    :return radius: diamètre du marqueur à afficher sur la carte
    :rtype radius: integer
    :return diflat: différence entre les deux latitudes extrêmes
    :rtype diflat: float
    :return diflong: différence entre les deux longitudes extrêmes
    :rtype diflong: float
    """
    # calcul de diflong, diflat, de la longitude et de la latitude moyenne sur la carte
    diflat = max(latlist) - min(latlist)
    diflong = max(longlist) - min(longlist)
    avglat = (max(latlist) + min(latlist)) / 2
    avglong = (max(longlist) + min(longlist)) / 2

    # définir les dimensions extrêmes de la carte
    if diflong > diflat:
        # si la largeur est plus grande que la longueur, longueur = 0.8 * largeur;
        # on centre la carte sur la longueur moyenne
        minlat = avglat - diflong * 0.8
        maxlat = avglat + diflong * 0.8
        sw = [minlat, min(longlist)]
        ne = [maxlat, max(longlist)]
    else:
        # si la longueur est plus grande que la largeur, largeur = 1.25 * longueur;
        # on centre la carte sur la largeur moyenne
        minlong = avglong - diflat * 1.25
        maxlong = avglong + diflat * 1.25
        sw = [min(latlist), minlong]
        ne = [max(latlist), maxlong]

    # définition de la taille des marqueurs, qui varie selon leur distance sur la carte
    if diflat > 50 or diflong > 50:
        radius = 300000
    elif diflat > 30 or diflong > 30:
        radius = 200000
    elif diflat > 5 or diflong > 5:
        radius = 50000
    elif diflat > 1 or diflong > 1:
        radius = 10000
    else:
        radius = 2000

    # return
    return sw, ne, radius, diflat, diflong
