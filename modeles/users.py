from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# from .. app import db,login #importer la base de donnée, l'application et le module Login
# du duchamp_reader


# en nommant seulement mes variables 'id', 'user'..., il est possible que je me farcisse des msg d'erreur bêbêtes
# puisque les variables sont redéfinies ailleurs
class User(UserMixin, db.Model):
    """
    La classe représentant les utilisateur.ices du duchamp_reader

    Attributs
    ---------
    :id: la clé primaire identifiant l'utilisateur.ice dans la base de données, générée automatiquement (data type : integer, obligatoire)
    :nom: le nom de l'utilisateur.ice (data type : text, obligatoire)
    :login: le login utilisé par l'utilisateur.ice (data type : text, longueur max : 45 caractères, obligatoire)
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
    login = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    authorships = db.relationship("Artiste", secondary=Authorship, back_populates="user")

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

        :param login:
        :param email:
        :param nom:
        :param mdp:
        :return: nouveau compte d'utilisateur.ice si 'True' ; liste d'erreurs si 'False'
        :rtype: objet User is 'True' ; list si 'False'
        """
        erreurs = []
        if not login:
            erreurs.append("Veuillez fournir un login.")
        if not email:
            erreurs.append("Veuillez fournir un email.")
        if not nom:
            erreurs.append("Veuillez fournir un nom d'utilisateur.ice.")
        if not mdp:
            erreurs.append("Veuillez fournir un mot de passe.")

        # vérifier que le mot de passe réponde à quelques consignes de sécurité
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

        # vérifier que l'email et le login sont ne sont pas déjà utilisés
        login_check = User.query.filter(User.login == login).count()
        if login_check > 0:
            erreurs.append("Ce login est déjà utilisé ; veuillez en choisir un autre.")
        email_check = User.query.filter(User.email == email).count()
        if email_check > 0:
            erreurs.append("Cette adresse mail est déjà utilisée. Veuillez en choisir une autre.")

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

#récupérer l'id de l'utilisateur.ice courant.e
@login.user_loader
def get_usr_by_id(identifiant):
    """Récupérer l'id de l'utilisateur.ice courant.e pour gérer les connexions actives.

    :param identifiant: l'identifiant de l'utilisateur.ice actuel.le
    :return: l'objet 'User' correspondant à cet identifiant
    """
    return User.query.get(int(identifiant))
