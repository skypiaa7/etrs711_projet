import sqlite3

class Etagere:
    def __init__(self, nom_etagere):
        self.nom_etagere = nom_etagere

    def ajouter_etagere(self, id_user, id_cave, nb_bouteille=0, nb_bouteille_dispo=15):
        
        #connection avec la base de donnée
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        #vérifie que le nom n'est pas déjà prit
        cursor.execute("SELECT * FROM etagere WHERE nom_etagere = ?", (self.nom_etagere,))
        result = cursor.fetchone()

        if result:
            print("cette étagère existe déjà, définissez un autre nom pour votre etagère")
            connection.close()

        else:
            cursor.execute("INSERT INTO Etagere (id_cave, nb_bouteille, nb_bouteille_dispo, nom_etagere, id_user) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (id_cave, nb_bouteille, nb_bouteille_dispo, self.nom_etagere, id_user))
            connection.commit()
            connection.close()

            print("etagere correctement ajouté")

    def liste_bouteilles(self):

        # Récupérer l'id de l'étagère en fonction de son nom
        nom_etagere = self.nom_etagere
        print (nom_etagere)
        id_etagere = self.get_id_etagere(nom_etagere)

        if id_etagere is not None:
            # Connexion à la base de données SQLite
            conn = sqlite3.connect('bouteille.db')
            cursor = conn.cursor()

            # Requête SQL avec jointure entre les tables Bouteille et Vin
            query = f"""
                SELECT Bouteille.*, Vin.*
                FROM Bouteille
                JOIN Vin ON Bouteille.id_vin = Vin.id_vin
                WHERE Bouteille.id_etagere = {id_etagere};
            """

            # Exécution de la requête SQL
            cursor.execute(query)

            # Récupération des résultats
            results = cursor.fetchall()

            print(results)
            # Affichage des résultats
            print("voici la liste de vois bouteille:")
            for row in results:
                print(row)

            #Fermeture de la connexion à la base de données
            conn.close()

    def get_id_etagere(self, nom_etagere):

        # Connexion à la base de données SQLite
        conn = sqlite3.connect('bouteille.db')
        cursor = conn.cursor()

        # Requête SQL pour récupérer l'id de l'étagère en fonction de son nom
        query = f"SELECT id_etagere FROM Etagere WHERE nom_etagere = '{nom_etagere}'"
        cursor.execute(query)

        # Récupération du résultat
        result = cursor.fetchone()

        if result:
            print (result[0])
            return result[0]
        else:
            print(f"Aucune étagère trouvée avec le nom '{nom_etagere}'")
            return None
        
        conn.close()

# Création d'une instance de la classe Etagere
nom_etagere_test = "etagere_1"
etagere_test = Etagere(nom_etagere_test)

# Appel de la méthode liste_bouteilles
etagere_test.liste_bouteilles()
