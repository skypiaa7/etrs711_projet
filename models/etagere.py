import sqlite3

class Etagere:
    def __init__(self, nom_etagere, id_user):
        self.nom_etagere = nom_etagere
        self.id_user = id_user

    def ajouter_etagere(self, id_cave, nb_bouteille=0, nb_bouteille_dispo=15):
        
        #connection avec la base de donnée
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        #vérifie que le nom n'est pas déjà prit
        cursor.execute("SELECT * FROM etagere WHERE nom_etagere = ? AND id_user = ?", (self.nom_etagere, self.id_user))
        result = cursor.fetchone()

        if result:
            print("cette étagère existe déjà, définissez un autre nom pour votre etagère")
            connection.close()
            return None

        else:
            cursor.execute("INSERT INTO Etagere (id_cave, nb_bouteille, nb_bouteille_dispo, nom_etagere, id_user) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (id_cave, nb_bouteille, nb_bouteille_dispo, self.nom_etagere, self.id_user))
            connection.commit()
            connection.close()

            print("etagere correctement ajouté")
        return True

    def liste_bouteilles(self):

        # Récupérer l'id de l'étagère en fonction de son nom
        id_etagere = self.get_id_etagere()

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

            # Fermeture de la connexion à la base de données
            conn.close()

            # Affichage des résultats
            for row in results:
                print(row)
        
        return results
    

    def get_id_etagere(self):

        # Connexion à la base de données SQLite
        conn = sqlite3.connect('bouteille.db')
        cursor = conn.cursor()

        # Requête SQL pour récupérer l'id de l'étagère en fonction de son nom
        query = f"SELECT id_etagere FROM Etagere WHERE nom_etagere = '{self.nom_etagere}' AND id_user = '{self.id_user}';"
        cursor.execute(query)

        # Récupération du résultat
        result = cursor.fetchone()

        if result:
            print (result[0])
            return result[0]
        else:
            print(f"Aucune étagère trouvée avec le nom '{self.nom_etagere}'")
            return None
        
        conn.close()
    
    def supprimer_etagere(self):
        # Connexion à la base de données SQLite
        conn = sqlite3.connect('bouteille.db')
        cursor = conn.cursor()

        # Vérifier si l'étagère existe
        cursor.execute("SELECT * FROM Etagere WHERE nom_etagere = ? AND id_user = ?", (self.nom_etagere,self.id_user))
        result = cursor.fetchone()

        if result is None:
            print("Etagère non trouvée.")
            return None
        else:
            # Supprimer toutes les bouteilles associées à l'étagère
            cursor.execute("DELETE FROM Bouteille WHERE id_etagere = ?", (result[0],))

            # Supprimer l'étagère
            cursor.execute("DELETE FROM Etagere WHERE nom_etagere = ?", (self.nom_etagere,))

            # Commit les changements et fermer la connexion
            conn.commit()
            conn.close()

            print("Etagère et toutes les bouteilles associées supprimées avec succès.")
            return True

# nvetagere = Etagere("test", 15)
# nvetagere.ajouter_etagere(1, 0, 15)
# nvetagere.liste_bouteilles()
# nvetagere.supprimer_etagere()


