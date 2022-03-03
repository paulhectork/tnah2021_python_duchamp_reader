from sqlalchemy_utils.functions import database_exists

from .app import db
from .routes import *
from .modeles import classes_users, classes_generic
# j'ai dû faire classes_users ça sinon j'avais une erreur:
# Missing user_loader or request_loader

def db_create():
    if not database_exists('sqlite:///db.sqlite'):
        db.create_all()

def db_populate_galerie():
    if not Galerie.query.get(1):
        Galerie.galerie_new_init("In-Situ Fabienne Leclerq", "http://insituparis.fr")
        Galerie.galerie_new_init("The Third Line", "https://www.thethirdline.com")
        Galerie.galerie_new_init("CRC", "https://www.charlesryanclarke.com/gallery")
        Galerie.galerie_new_init("Michael Rein", "https://michelrein.com/")
        Galerie.galerie_new_init("Peter Kleichman", "https://www.peterkilchmann.com/")
        Galerie.galerie_new_init("Marcelle Alix", "http://www.marcellealix.com/")
        Galerie.galerie_new_init("Thomas Bernard - Cortex Athletico", "https://www.galeriethomasbernard.com/")
        Galerie.galerie_new_init("Counter Space", "https://www.counterspacegallery.com/")
        Galerie.galerie_new_init("Eva Hober", "http://www.evahober.com/")
        Galerie.galerie_new_init("Reinhard Hauff", "https://www.instagram.com/galeriereinhardhauff/")
        Galerie.galerie_new_init("kammel mennour", "https://kamelmennour.com/")
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
        Galerie.galerie_new_init("CulturesInterface", "https://www.facebook.com/pages/category/Art-Gallery/CulturesInterface-327265323963197/")
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

def db_populate_ville():
    if not Ville.query.get(1):
        Ville.ville_new_init("Alfortville", 48.80516, 2.41971, "France")
        Ville.ville_new_init("Aurillac", 44.92854, 2.44331, "44.92854 2.44331")
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
        Ville.ville_new_init("Hamilton", 32.29561, -64.78270, "Canada")
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
        Ville.ville_new_init("Sarajevo", 43.85198, 18.38669, "Bosine-Herzégovine")
        Ville.ville_new_init("Ris-Orangis", 48.65388, 2.41512, "France")
        Ville.ville_new_init("Rome", 41.89332, 12.48293, "Italie")
        Ville.ville_new_init("Salt Lake City", 40.75962, -111.88680, "Etats-Unis d'Amérique")
        Ville.ville_new_init("Santiago", -33.43778, -70.65045, "Chili")
        Ville.ville_new_init("Stuttgart", 48.77845, 9.18001, "Allemagne")
        Ville.ville_new_init("Varsovie", 52.23372, 21.07143, "Pologne")
        Ville.ville_new_init("Vienne", 48.20835, 16.37250, "Autriche")
        Ville.ville_new_init("Zurich", 47.37445, 8.54104, "Suisse")
        Ville.ville_new_init("Zuoz", 46.60129, 9.96080, "Suisse")

# def db_populate_theme
# def db_populate_nomination
# def db_populate_relation_represente
# def db_populate_relation_localisation

def db_populate():
    if not Artiste.query.get(1):
        Artiste.artiste_new_init("Fontaine", "Claire", 1985, "F", 1, 1)
    db_populate_galerie()
    db_populate_ville()
