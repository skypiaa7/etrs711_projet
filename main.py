import sqlite3  # Vous pouvez utiliser la bibliothèque appropriée pour votre base de données

class Bouteille:
    def __init__(self, name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso):
        self.name = name
        self.domaine = domaine
        self.type = type
        self.annee = annee
        self.region = region
        self.commentaire = commentaire
        self.prix = prix
        self.note_commu = note_commu
        self.note_perso = note_perso

    def ajouter_modele_bouteille(self):
        # Établir une connexion à la base de données (assurez-vous d'avoir créé la table Bouteille)
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        # Vérifier si le modèle de bouteille existe déjà dans la base
        cursor.execute("SELECT id_bouteille FROM Bouteille WHERE name=? AND domaine=? AND type=? AND annee=?",
                       (self.name, self.domaine, self.type, self.annee))
        existing_bouteille = cursor.fetchone()

        if existing_bouteille:
            print("Le modèle de bouteille existe déjà.")
            connection.close()
        else:
            # Insérer un nouveau modèle de bouteille
            cursor.execute("INSERT INTO Bouteille (name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso)"
                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.name, self.domaine, self.type, self.annee, self.region, self.commentaire,
                            self.prix, self.note_commu, self.note_perso))

            # Committer les changements et fermer la connexion
            connection.commit()
            connection.close()
            print("Modèle de bouteille ajouté avec succès.")

class MesBouteilles:
    def __init__(self, id_bouteille, id_etagere, column_name, note_perso, qt_totale):
        self.id_bouteille = id_bouteille
        self.id_etagere = id_etagere
        self.column_name = column_name
        self.note_perso = note_perso
        self.qt_totale = qt_totale

    def ajouter_bouteille(self):
        # Ajouter la logique pour ajouter une bouteille dans la table MesBouteilles
        # Vérifier si la bouteille existe déjà dans la table Bouteille
        # Si non, ajouter la bouteille dans la table Bouteille
        # Ajouter la bouteille dans la table MesBouteilles avec l'id de l'étagère
        # Si la bouteille existe déjà dans MesBouteilles, augmenter la quantité de 1
        pass

    def supprimer_bouteille(self):
        # Ajouter la logique pour supprimer une bouteille de la table MesBouteilles
        # Si la quantité est supérieure à 1, réduire la quantité de 1
        pass

# Exemple d'utilisation
# Création d'une instance de la classe Bouteille
nouvelle_bouteille = Bouteille(
    name="cote du rhone",
    domaine="Domaine de l'Échantillon",
    type="Rouge",
    annee=2019,
    region="Bordeaux",
    commentaire="Un vin rouge délicieux",
    prix=25,
    note_commu=4,
    note_perso=5
)

# Appel de la méthode pour ajouter le modèle de bouteille dans la base de données
nouvelle_bouteille.ajouter_modele_bouteille()

# bouteille1.ajouter_modele_bouteille()

# mes_bouteilles1 = MesBouteilles(id_bouteille, id_etagere, column_name, note_perso, qt_totale)
# mes_bouteilles1.ajouter_bouteille()
# mes_bouteilles1.supprimer_bouteille()
