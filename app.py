from models.user import User
from models.vin import Vin
from models.bouteille import Bouteille
from models.etagere import Etagere
# vin_manager/app.py
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret'
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

login_manager.init_app(app)
login_manager.login_view = 'login'

vin_instance = Vin(None, None, None, None, None, None, None, None, None)
print("le programme commence")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cave')
@login_required
def cave():
    return render_template('cave.html')


@app.route('/vin', methods=['GET', 'POST'])
@login_required
def vin():
    if request.method == 'POST':
        # Récupérez les données du formulaire
        name = request.form['name']
        domaine = request.form['domaine']
        type = request.form['type']
        annee = request.form['annee']
        region = request.form['region']
        commentaire = request.form['commentaire']
        prix = request.form['prix']
        note_commu = request.form['note_commu']
        note_perso = request.form['note_perso']

        # Mettez à jour les valeurs de l'instance Vin avec les données du formulaire
        vin_instance.name = name
        vin_instance.domaine = domaine
        vin_instance.type = type
        vin_instance.annee = annee
        vin_instance.region = region
        vin_instance.commentaire = commentaire
        vin_instance.prix = prix
        vin_instance.note_commu = note_commu
        vin_instance.note_perso = note_perso

        # Ajoutez le vin en utilisant la méthode ajouter_vin de la classe Vin
        vin_instance.ajouter_vin()

        # Redirigez vers la page de confirmation
        return render_template('ajouter_vin.html')

@app.route('/bouteille')
@login_required
def bouteille():
    return render_template('bouteille.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.authentification_user():
            login_user(user)
            print(user.id)  # Imprimer l'ID de l'utilisateur
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)





