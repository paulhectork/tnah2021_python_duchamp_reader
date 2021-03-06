from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..app import db, login  # importer la base de donnée, l'application et le LoginManager() du duchamp_reader
from ..utils.regex import *


class User(UserMixin, db.Model):
    """
    La classe représentant les utilisateur.ices du duchamp_reader

    Attributs
    ---------
    :id: la clé primaire identifiant l'utilisateur.ice dans la base de données, générée automatiquement (data type : integer, obligatoire)
    :nom: le nom de l'utilisateur.ice (data type : text, obligatoire)
    :login: le login/nom d'utilisateur.ice utilisé par l'utilisateur.ice (data type : text, longueur max : 45 caractères, obligatoire)
    :email: l'adresse mail utilisée par l'utilisateur.ice (data type : text, obligatoire)
    :password: le mot de passe utilisé par l'utilisateur.ice (data type : text, longueur max : 100, obligatoire)

    Static methods
    --------------
    :usr_connexion(login, mdp): connecter l'utilisateur.ice
    :usr_new(login, email, nom, mdp): créer un compte d'utilisateur.ice

    Methods
    -------
    :get_id(self): récupérer l'ID de l'utilisateur.ice courant.e

    """
    __tablename__ = "user"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    login = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    authorship_artiste = db.relationship("AuthorshipArtiste", back_populates="user")
    authorship_nomination = db.relationship("AuthorshipNomination", back_populates="user")
    authorship_galerie = db.relationship("AuthorshipGalerie", back_populates="user")
    authorship_ville = db.relationship("AuthorshipVille", back_populates="user")
    authorship_theme = db.relationship("AuthorshipTheme", back_populates="user")

    @staticmethod
    def usr_connexion(login, mdp):
        """Identifier un.e utilisateur.ice lorsqu'il/elle se connecte.
        Retourner les données de l'utilisateur.ice si son login et son mot de passe sont corrects.

        :param login: login de l'utilisateur.ice
        :param mdp: login de l'utilisateur.ice
        :returns: les données de l'utilisateur.ice si le login et mdp sont corrects; sinon, None
        :rtype: User ou None
        """
        user = User.query.filter(User.login == login).first()
        if user and check_password_hash(user.password, mdp):
            return user
        return None

    @staticmethod
    def usr_new(login, email, nom, mdp):
        """Créer un compte pour un.e nouvel.le utilisateur.ice. Si le login, email, nom ou mdp
        fournis ne conviennent pas, ne pas créer de compte et afficher la liste d'erreurs. Si tout
        va bien, créer un nouvel utilisateur, l'ajouter à la base de données et renvoyer les données
        de l'utilisateur.

        :param login: nom utilisé par l'utilisateur.ice
        :param email: email de l'utilisateur.ice
        :param nom: nom civil de l'utilisateur.ice
        :param mdp: mot de pase de l'utilisateur.ice
        :return: nouveau compte d'utilisateur.ice si 'True' ; liste d'erreurs si 'False'
        :rtype: objet User si 'True' ; list si 'False'
        """
        erreurs = []
        if not login:
            erreurs.append("Veuillez fournir un nom d'utilisateur.ice")
        if not email:
            erreurs.append("Veuillez fournir un email")
        if not nom:
            erreurs.append("Veuillez fournir un nom d'utilisateur.ice")
        if not mdp:
            erreurs.append("Veuillez fournir un mot de passe")

        # vérifier les données sont valides
        nom = clean_string(nom)
        nomregex = re.search(regexnp, nom)
        if not nomregex:
            erreurs.append(
                "Votre nom doit correspondre à l'expression: \
                ^[A-Z]((([a-z]')|[-\s]|[A-Z])*([àáâäéèêëíìîïòóôöúùûüøœæ&+]|[a-z])+)+[^-]$ \
                (majuscules non-accentuées uniquement et obligatoirement en début de mot, lettres accentuées ou non, \
                tirets et espaces, miniscule en fin de chaîne)"
            )
        emailregex = re.search(regexmail, email)
        if not emailregex:
            erreurs.append("Veuillez fournir un email valide")
        # les mots de passe doivent contenir 8 caractères dont un chiffre au moins
        mdp2 = ""
        for character in mdp:
            mdp2 += character
            mdp2 += " "
        chiffres = []
        for chiffre in range(10):
            chiffres.append(str(chiffre))
        if len(mdp) < 8 and not any(chiffre in mdp2 for chiffre in chiffres):
            erreurs.append("Votre mot de passe doit contenir au moins 8 caractères dont un chiffre !")
        elif len(mdp) < 8:
            erreurs.append("Votre mot de passe doit contenir au moins 8 caractères !")
        elif len(mdp) > 8 and not any(chiffre in mdp2 for chiffre in chiffres):
            erreurs.append("Votre mot de passe doit contenir au moins un chiffre !")

        # vérifier que l'email et le login ne sont pas déjà utilisés
        db_login_check = User.query.filter(User.login == login).count()
        if db_login_check > 0:
            erreurs.append("Ce nom d'utilisateur.ice est déjà utilisé ; veuillez en choisir un autre")
        db_email_check = User.query.filter(User.email == email).count()
        if db_email_check > 0:
            erreurs.append("Cette adresse mail est déjà utilisée. Veuillez en choisir une autre")

        # vérifier qu'il n'y a pas d'erreurs dans la création de compte
        if len(erreurs) > 0:
            return False, erreurs

        # si il n'y a pas d'erreurs, créer un utilisateur
        nv_utilisateur = User(
            nom=nom,
            login=login,
            email=email,
            password=generate_password_hash(mdp)
        )

        # ajouter l'utilisateur à la base de données
        try:
            db.session.add(nv_utilisateur)
            db.session.commit()
            return True, nv_utilisateur
        except Exception as error:
            return False, [str(error)]

    def get_id(self):
        """Retourne l'id de l'utilisateur.ice actuellement connecté.e

        :return: ID de l'utilisateur.ice
        :rtype: int
        """
        return self.id



# récupérer l'id de l'utilisateur.ice courant.e et gérer les connexions actives

@login.user_loader # IL Y A UNE ERREUR A CET ENDROIT MAIS FUCK IF I KNOW WHY
def load_user(user_id):
    """Configurer l'user_loader: récupérer l'id de l'utilisateur.ice courant.e pour gérer les connexions actives.

    :param identifiant: l'identifiant de l'utilisateur.ice actuel.le
    :return: l'objet 'User' correspondant à cet identifiant
    """
    return User.query.get(int(user_id))
