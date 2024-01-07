import sqlite3

class Vin:
    def __init__(self, name, domaine, type, annee, region, commentaire, prix, note_commu):
        self.name = name
        self.domaine = domaine
        self.type = type
        self.annee = annee
        self.region = region
        self.commentaire = commentaire
        self.prix = prix
        self.note_commu = note_commu

    def ajouter_vin(self):
        # Établir une connexion à la base de données (assurez-vous d'avoir créé la table Bouteille)
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        # Vérifier si le modèle de bouteille existe déjà dans la base
        cursor.execute("SELECT id_vin FROM Vin WHERE name=? AND domaine=? AND type=? AND annee=?",
                        (self.name, self.domaine, self.type, self.annee))
        existing_vin = cursor.fetchone()

        if existing_vin:
            print("Le modèle de vin existe déjà.")
            print(existing_vin[0])
            connection.close()
        else:
            # Insérer un nouveau modèle de bouteille
            cursor.execute("INSERT INTO Vin (name, domaine, type, annee, region, commentaire, prix, note_commu)"
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (self.name, self.domaine, self.type, self.annee, self.region, self.commentaire,
                            self.prix, self.note_commu))

            # Committer les changements et fermer la connexion
            connection.commit()
            connection.close()
            print("Modèle de bouteille ajouté avec succès.")
    
        

    @staticmethod
    def list_vin():
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM Vin;
        '''
        result = cursor.execute(query).fetchall()
        connection.close()
        return result
