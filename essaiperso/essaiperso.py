"""
about: ce magnifique projet sublime projet permet de sélectionner un élément d'une liste de formulaire
       et de le retourner ; ce quo est retourné : une chaîne de caractères qui correspond au contenu textuel de l'élément <option>
       comment on fait: on stocke ce qu'on veut retourner dans une variable (ici saperlipopette) que l'on met entre {{}} dans la template
"""

from flask import Flask, render_template, request, flash

app = Flask(
    "Application",
    template_folder="templates"
)
app.config['SECRET_KEY'] = "a"

@app.route("/", methods=["GET", "POST"])
def form_select():
    if request.method == "POST":
        objet = request.form.get("test_select", None)
        print(objet)
        print(type(objet))
        flash("tout va bien mon lapin")
        return render_template("essaiperso.html", saperlipopette=objet)
    else:
        return render_template("essaiperso.html", saperlipopette="rien pour le moment ; veuillez envoyer un formulaire")

if __name__ == "__main__":
    app.run()