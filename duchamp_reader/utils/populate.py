from sqlalchemy_utils.functions import database_exists

from ..app import db
from ..modeles.classes_generic import Artiste, Galerie, Nomination, Theme, Ville
from ..modeles.classes_relationships import RelationRepresente, RelationLocalisation

def db_create():
    """Fonction d'initalisation permettant de créer la base de donnéres
    """
    if not database_exists('sqlite:///db.sqlite'):
        print("")
        print("###########################################")
        print("CRÉATION DE LA BASE DE DONNÉES")
        db.create_all()

def db_populate_galerie():
    """Fonction d'initialisation permettant de peupler la table Galerie
    """
    if not Galerie.query.get(1):
        Galerie.galerie_new_init("In-Situ Fabienne Leclerq", "http://insituparis.fr")
        Galerie.galerie_new_init("The Third Line", "https://www.thethirdline.com")
        Galerie.galerie_new_init("Charles Ryan Clarke", "https://www.charlesryanclarke.com/gallery")
        Galerie.galerie_new_init("Michael Rein", "https://michelrein.com/")
        Galerie.galerie_new_init("Peter Kleichman", "https://www.peterkilchmann.com/")
        Galerie.galerie_new_init("Marcelle Alix", "http://www.marcellealix.com/")
        Galerie.galerie_new_init("Thomas Bernard - Cortex Athletico", "https://www.galeriethomasbernard.com/")
        Galerie.galerie_new_init("Counter Space", "https://www.counterspacegallery.com/")
        Galerie.galerie_new_init("Eva Hober", "http://www.evahober.com/")
        Galerie.galerie_new_init("Reinhard Hauff", "https://www.instagram.com/galeriereinhardhauff/")
        Galerie.galerie_new_init("Kammel Mennour", "https://kamelmennour.com/")
        Galerie.galerie_new_init("Meessen de Clerq", "https://www.meessendeclercq.be/")
        Galerie.galerie_new_init("Greta Meert", "https://galeriegretameert.com/")
        Galerie.galerie_new_init("Barbara Wien", "https://www.barbarawien.de/")
        Galerie.galerie_new_init("Juana de Aizpuru", "http://juanadeaizpuru.es/")
        Galerie.galerie_new_init("Jocelyn Wolff", "http://www.galeriewolff.com/gallery")
        Galerie.galerie_new_init("Meyer Riegger", "https://meyer-riegger.de/en")
        Galerie.galerie_new_init("Clearing", "http://www.c-l-e-a-r-i-n-g.com/")
        Galerie.galerie_new_init("Almine Reich", "https://www.alminerech.com/")
        Galerie.galerie_new_init("Max Helzer", "https://www.maxhetzler.com/")
        Galerie.galerie_new_init("Alfonso Artiaco", "https://www.alfonsoartiaco.com/en")
        Galerie.galerie_new_init("Petro Sparta", "https://www.artbasel.com/catalog/gallery/2906/Galerie-Pietro-Spart%C3%A0")
        Galerie.galerie_new_init("Jérôme Poggi", "http://galeriepoggi.com/")
        Galerie.galerie_new_init("Goodman Gallery", "https://www.goodman-gallery.com/")
        Galerie.galerie_new_init("Tanja Wagner", "https://tanjawagner.com/")
        Galerie.galerie_new_init("Valérie Bach - La Patinoire Royale", "https://www.prvbgallery.com/")
        Galerie.galerie_new_init("Wentrup", "https://wentrupgallery.com/en")
        Galerie.galerie_new_init("Cultures Interface", "https://www.facebook.com/pages/category/Art-Gallery/CulturesInterface-327265323963197/")
        Galerie.galerie_new_init("Emmanuel Layr", "https://emanuellayr.com/")
        Galerie.galerie_new_init("Dittrich & Schlechtreim", "https://dittrich-schlechtriem.com/")
        Galerie.galerie_new_init("Sean Kelly", "https://www.skny.com/")
        Galerie.galerie_new_init("Sies + Höke", "https://www.sieshoeke.com/")
        Galerie.galerie_new_init("Tschudi", "https://www.galerie-tschudi.ch/")
        Galerie.galerie_new_init("Balice Hertling", "https://www.balicehertling.com/")
        Galerie.galerie_new_init("Francesca Pia", "https://www.francescapia.com")
        Galerie.galerie_new_init("Hannah Hoffman", "https://www.hannahhoffman.la/")
        Galerie.galerie_new_init("Foskal", "https://www.galeriafoksal.pl/en/home/")
        Galerie.galerie_new_init("High Art", "https://highart.fr/")
        Galerie.galerie_new_init("Document", "https://documentspace.com/")
        print("TABLE 'GALERIE' PEUPLÉE")

def db_populate_ville():
    """Fonction d'initialisation permettant de peupler la table Ville
    """
    if not Ville.query.get(1):
        Ville.ville_new_init("Alfortville", 48.80516, 2.41971, "France")
        Ville.ville_new_init("Aurillac", 44.92854, 2.44331, "France")
        Ville.ville_new_init("Belgrade", 44.81781, 20.45690, "Serbia")
        Ville.ville_new_init("Berlin", 52.51704, 13.38886, "Allemagne")
        Ville.ville_new_init("Beyrouth", 33.88894, 35.49442,"Liban")
        Ville.ville_new_init("Bilda", 36.4666648, 2.8166634, "Algérie")
        Ville.ville_new_init("Bruxelles", 50.85397, 4.35266, "Belgique")
        Ville.ville_new_init("Carshalton", 51.36579, -0.16109, "Royaume-Uni")
        Ville.ville_new_init("Casablanca", 33.59506, -7.61878, "Maroc")
        Ville.ville_new_init("Chagny", 46.89960, 4.78119, "France")
        Ville.ville_new_init("Chicago", 41.87556, -87.62442, "Etats-Unis d'Amérique")
        Ville.ville_new_init("Cholet", 47.06173, -0.88013, "France")
        Ville.ville_new_init("Colmar", 48.07740, 7.35190, "France")
        Ville.ville_new_init("Dijon", 47.32158, 5.04147, "France")
        Ville.ville_new_init("Dubai", 25.26535, 55.29249, "Emirats-Arabes-Unis")
        Ville.ville_new_init("Dusseldorf", 51.22540, 6.77631, "Allemagne")
        Ville.ville_new_init("Fontenay-sous-Bois", 48.85028, 2.47325, "France")
        Ville.ville_new_init("Francfort-sur-le-Main", 50.11064, 8.68209, "Allemagne")
        Ville.ville_new_init("Genève", 46.20176, 6.14660, "Suisse")
        Ville.ville_new_init("Grenoble", 45.18756, 5.73578, "France")
        Ville.ville_new_init("Hamilton", 43.25011, -79.84963, "Canada")
        Ville.ville_new_init("Ho Chi Minh-City", 10.77155, 106.69838, "Vietnam")
        Ville.ville_new_init("Johannesburg", -26.20500, 28.04972, "France")
        Ville.ville_new_init("Karlsruhe", 49.00687, 8.40342, "Allemagne")
        Ville.ville_new_init("La Rochelle", 46.15911, -1.15204, "France")
        Ville.ville_new_init("Le Blanc-Mesnil", 48.93855, 2.46315, "France")
        Ville.ville_new_init("Londres", 51.50732, -0.12765,"Royaume-Uni")
        Ville.ville_new_init("Los Angeles", 34.05369, -118.24277, "Etats-Unis d'Amérique")
        Ville.ville_new_init("Madrid", 40.41670, -3.70358, "Espagne")
        Ville.ville_new_init("Morges", 46.50933, 6.49832, "Suisse")
        Ville.ville_new_init("Naples", 40.83588, 14.24877, "Italie")
        Ville.ville_new_init("New York", 40.71273, -74.00602, "Etats-Unis d'Amérique")
        Ville.ville_new_init("Paris", 48.85889, 2.32004, "France")
        Ville.ville_new_init("Ris-Orangis", 48.65388, 2.41512, "France")
        Ville.ville_new_init("Rome", 41.89332, 12.48293, "Italie")
        Ville.ville_new_init("Salt Lake City", 40.75962, -111.88680, "Etats-Unis d'Amérique")
        Ville.ville_new_init("Santiago", -33.43778, -70.65045, "Chili")
        Ville.ville_new_init("Sarajevo", 43.85198, 18.38669, "Bosine-Herzégovine")
        Ville.ville_new_init("Stuttgart", 48.77845, 9.18001, "Allemagne")
        Ville.ville_new_init("Varsovie", 52.23372, 21.07143, "Pologne")
        Ville.ville_new_init("Vienne", 48.20835, 16.37250, "Autriche")
        Ville.ville_new_init("Zurich", 47.37445, 8.54104, "Suisse")
        Ville.ville_new_init("Zuoz", 46.60129, 9.96080, "Suisse")
        print("TABLE 'VILLE' PEUPLÉE")

def db_populate_theme():
    """Fonction d'initialisation permettant de peupler la table Theme
    """
    if not Theme.query.get(1):
        Theme.theme_new_init("mondialisation - migrations - décolonialisme")
        Theme.theme_new_init("féminisme - identité de genre")
        Theme.theme_new_init("médias - images")
        Theme.theme_new_init("écologie - sciences - anthropocène")
        Theme.theme_new_init("mémoire - histoire")
        Theme.theme_new_init("abstraction - formalisme")
        print("TABLE 'THÈME' PEUPLÉE")

def db_populate_artiste():
    """Fonction d'initialisation permettant de peupler la table Artiste
    """
    if not Artiste.query.get(1):
        Artiste.artiste_new_init("Hadjithomas", "Joana", 1969, "F", "Q3179639", 5, 5)
        Artiste.artiste_new_init("Bajevic", "Maja", 1967, "F", "Q1491703", 38, 33)
        Artiste.artiste_new_init("Moth", "Charlotte", 1978, "F", "Q23415099", 8, 33)
        Artiste.artiste_new_init("Santoro", "Vittorio", 1962, "M", "Q1565174", 42, 42)
        Artiste.artiste_new_init("Cogitore", "Clément", 1962, "M", "Q21055548", 13, 33)
        Artiste.artiste_new_init("Bourouissa", "Mohamed", 1978, "M", "Q3318456", 6, 33)
        Artiste.artiste_new_init("Tran", "Thu-Van", 1979, "F", "Q25936115", 22, 33)
        Artiste.artiste_new_init("Voignier", "Marie", 1974, "F", "Q28777080", 34, 33)
        Artiste.artiste_new_init("Baudelaire", "Eric", 1973, "M", "Q3590965", 36, 33)
        Artiste.artiste_new_init("Bock", "Katinka", 1976, "F", "Q19513339", 18, 4)
        Artiste.artiste_new_init("Humeau", "Marguerite", 1986, "F", "Q25324799", 12, 27)
        Artiste.artiste_new_init("Tursic", "Ida", 1974, "F", id_wikidata=None,
                                 id_ville_naissance=3, id_ville_residence=14)
        Artiste.artiste_new_init("Kiwanga", "Kapwani", 1978, "F", "Q22978214", 21, 33)
        Artiste.artiste_new_init("Anderson", "Alice", 1972, "F", "Q2646836", 1, 27)
        Artiste.artiste_new_init("Berrada", "Hicham", 1986, "M", "Q18610848", 9, 33)
        Artiste.artiste_new_init("Ramirez", "Enrique", 1979, "M", "Q77350250", 37, 37)
        Artiste.artiste_new_init("Reynaud Dewar", "Lili", 1974, "F", "Q19630875", 25, 20)
        Artiste.artiste_new_init("Charrière", "Julian", 1987, "M", "Q17305541", 30, 4)
        Artiste.artiste_new_init("Cornaro", "Isabelle", 1974, "F", "Q55235943", 2, 19)
        Artiste.artiste_new_init("Creuzet", "Julien", 1986, "M", id_wikidata=None,
                                 id_ville_naissance=26, id_ville_residence=17)
        print("TABLE 'ARTISTE' PEUPLÉE")

def db_populate_nomination():
    """Fonction d'initialisation permettant de peupler la table Nomination
    """
    if not Nomination.query.get(1):
        Nomination.nomination_new_init(2017, True, 1, 1)
        Nomination.nomination_new_init(2017, False, 2, 5)
        Nomination.nomination_new_init(2017, False, 3, 3)
        Nomination.nomination_new_init(2017, False, 4, 6)
        Nomination.nomination_new_init(2018, True, 5, 5)
        Nomination.nomination_new_init(2018, False, 6, 1)
        Nomination.nomination_new_init(2018, False, 7, 1)
        Nomination.nomination_new_init(2018, False, 8, 1)
        Nomination.nomination_new_init(2019, True, 9, 3)
        Nomination.nomination_new_init(2019, False, 10, 5)
        Nomination.nomination_new_init(2019, False, 11, 4)
        Nomination.nomination_new_init(2019, False, 12, 3)
        Nomination.nomination_new_init(2020, True, 13, 1)
        Nomination.nomination_new_init(2020, False, 14, 5)
        Nomination.nomination_new_init(2020, False, 15, 4)
        Nomination.nomination_new_init(2020, False, 16, 1)
        Nomination.nomination_new_init(2021, True, 17, 2)
        Nomination.nomination_new_init(2021, False, 18, 4)
        Nomination.nomination_new_init(2021, False, 19, 3)
        Nomination.nomination_new_init(2021, False, 20, 1)
        print("TABLE 'NOMINATION' PEUPLÉE")

def db_populate_relation_represente():
    """Fonction d'initialisation permettant de peupler la table Represente
    """
    if not RelationRepresente.query.get(1):
        RelationRepresente.represente_new(1, 1)
        RelationRepresente.represente_new(1, 2)
        RelationRepresente.represente_new(1, 3)
        RelationRepresente.represente_new(2, 4)
        RelationRepresente.represente_new(2, 5)
        RelationRepresente.represente_new(3, 6)
        RelationRepresente.represente_new(4, 7)
        RelationRepresente.represente_new(4, 8)
        RelationRepresente.represente_new(5, 9)
        RelationRepresente.represente_new(5, 10)
        RelationRepresente.represente_new(6, 11)
        RelationRepresente.represente_new(7, 12)
        RelationRepresente.represente_new(8, 6)
        RelationRepresente.represente_new(9, 13)
        RelationRepresente.represente_new(9, 14)
        RelationRepresente.represente_new(9, 15)
        RelationRepresente.represente_new(10, 16)
        RelationRepresente.represente_new(10, 17)
        RelationRepresente.represente_new(11, 18)
        RelationRepresente.represente_new(12, 19)
        RelationRepresente.represente_new(12, 20)
        RelationRepresente.represente_new(12, 21)
        RelationRepresente.represente_new(12, 22)
        RelationRepresente.represente_new(13, 23)
        RelationRepresente.represente_new(13, 24)
        RelationRepresente.represente_new(13, 25)
        RelationRepresente.represente_new(14, 26)
        RelationRepresente.represente_new(15, 11)
        RelationRepresente.represente_new(15, 27)
        RelationRepresente.represente_new(15, 28)
        RelationRepresente.represente_new(16, 4)
        RelationRepresente.represente_new(17, 18)
        RelationRepresente.represente_new(17, 29)
        RelationRepresente.represente_new(18, 30)
        RelationRepresente.represente_new(18, 31)
        RelationRepresente.represente_new(18, 32)
        RelationRepresente.represente_new(18, 33)
        RelationRepresente.represente_new(19, 34)
        RelationRepresente.represente_new(19, 35)
        RelationRepresente.represente_new(19, 36)
        RelationRepresente.represente_new(19, 37)
        RelationRepresente.represente_new(20, 38)
        RelationRepresente.represente_new(20, 39)
        print("TABLE 'RELATIONREPRESENTE' PEUPLÉE")

def db_populate_relation_localisation():
    """Fonction d'initialisation permettant de peupler la table Localisation
    """
    if not RelationLocalisation.query.get(1):
        RelationLocalisation.localisation_new(1, 33)
        RelationLocalisation.localisation_new(2, 15)
        RelationLocalisation.localisation_new(3, 31)
        RelationLocalisation.localisation_new(4, 7)
        RelationLocalisation.localisation_new(4, 33)
        RelationLocalisation.localisation_new(5, 42)
        RelationLocalisation.localisation_new(6, 33)
        RelationLocalisation.localisation_new(7, 33)
        RelationLocalisation.localisation_new(8, 42)
        RelationLocalisation.localisation_new(9, 33)
        RelationLocalisation.localisation_new(10, 39)
        RelationLocalisation.localisation_new(11, 33)
        RelationLocalisation.localisation_new(11, 27)
        RelationLocalisation.localisation_new(12, 7)
        RelationLocalisation.localisation_new(13, 7)
        RelationLocalisation.localisation_new(14, 7)
        RelationLocalisation.localisation_new(15, 29)
        RelationLocalisation.localisation_new(16, 33)
        RelationLocalisation.localisation_new(17, 7)
        RelationLocalisation.localisation_new(17, 24)
        RelationLocalisation.localisation_new(18, 7)
        RelationLocalisation.localisation_new(19, 33)
        RelationLocalisation.localisation_new(19, 7)
        RelationLocalisation.localisation_new(19, 27)
        RelationLocalisation.localisation_new(19, 32)
        RelationLocalisation.localisation_new(20, 7)
        RelationLocalisation.localisation_new(21, 31)
        RelationLocalisation.localisation_new(22, 10)
        RelationLocalisation.localisation_new(23, 33)
        RelationLocalisation.localisation_new(24, 23)
        RelationLocalisation.localisation_new(25, 7)
        RelationLocalisation.localisation_new(26, 7)
        RelationLocalisation.localisation_new(27, 7)
        RelationLocalisation.localisation_new(28, 9)
        RelationLocalisation.localisation_new(29, 41)
        RelationLocalisation.localisation_new(29, 35)
        RelationLocalisation.localisation_new(30, 7)
        RelationLocalisation.localisation_new(31, 32)
        RelationLocalisation.localisation_new(32, 16)
        RelationLocalisation.localisation_new(33, 43)
        RelationLocalisation.localisation_new(34, 33)
        RelationLocalisation.localisation_new(35, 42)
        RelationLocalisation.localisation_new(36, 28)
        RelationLocalisation.localisation_new(37, 40)
        RelationLocalisation.localisation_new(38, 33)
        RelationLocalisation.localisation_new(39, 11)
        print("TABLE 'RELATIONLOCALISATION' PEUPLÉE")
        print("BASE DE DONNÉES CRÉÉE")
        print("###########################################")
        print("")

def db_populate():
    db_populate_galerie()
    db_populate_ville()
    db_populate_theme()
    db_populate_artiste()
    db_populate_nomination()
    db_populate_relation_represente()
    db_populate_relation_localisation()
