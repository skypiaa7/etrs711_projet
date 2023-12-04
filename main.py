import sqlite3 

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def get_user_id(self):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = '''
            SELECT id_user FROM User WHERE name = ? AND password = ?;
        '''
        result = cursor.execute(query, (self.name, self.password)).fetchone()
        if result:
            user_id = result[0]
            print(f"ID de l'utilisateur ({self.name}): {user_id}")
            return user_id
        else:
            print("Utilisateur non trouvé. Vérifiez le nom d'utilisateur et le mot de passe.")
            return None
        connection.close()


    def ajouter_user(self):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = '''
            INSERT INTO User (name, password) VALUES (?, ?);
        '''
        cursor.execute(query, (self.name, self.password))
        connection.commit()
        print(f"Utilisateur {self.name} ajouté avec succès.")
        connection.close()

    def supprimer_user(self):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        user_id = self.get_user_id()

        # Supprimer toutes les bouteilles associées aux étagères de l'utilisateur
        query_delete_bottles = '''
            DELETE FROM Bouteille
            WHERE id_etagere IN (
                SELECT id_etagere FROM Etagere WHERE id_user = ?
            );
        '''
        self.conn.execute(query_delete_bottles, (user_id,))

        # Supprimer toutes les étagères de l'utilisateur
        query_delete_shelves = '''
            DELETE FROM Etagere WHERE id_user = ?;
        '''
        self.conn.execute(query_delete_shelves, (user_id,))

        #supprime l'utilisateur 
        query = '''
            DELETE FROM User WHERE id_user = ?;
        '''
        cursor.execute(query, (user_id,))
        connection.commit()
        print(f"Utilisateur avec l'ID {user_id} supprimé avec succès.")
        connection.close()

    def authentification_user(self):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM User WHERE name = ? AND password = ?;
        '''
        result = cursor.execute(query, (self.name, self.password)).fetchone()
        if result:
            print("Authentification réussie.")
            return True
        else:
            print("Échec de l'authentification. Nom d'utilisateur ou mot de passe incorrect.")
            return False
        connection.close()

class Vin:
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

    def ajouter_vin(self):
        # Établir une connexion à la base de données (assurez-vous d'avoir créé la table Bouteille)
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        # Vérifier si le modèle de bouteille existe déjà dans la base
        cursor.execute("SELECT id_vin FROM Vin WHERE name=? AND domaine=? AND type=? AND annee=?",
                       (self.name, self.domaine, self.type, self.annee))
        existing_bouteille = cursor.fetchone()

        if existing_bouteille:
            print("Le modèle de bouteille existe déjà.")
            connection.close()
        else:
            # Insérer un nouveau modèle de bouteille
            cursor.execute("INSERT INTO Vin (name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso)"
                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.name, self.domaine, self.type, self.annee, self.region, self.commentaire,
                            self.prix, self.note_commu, self.note_perso))

            # Committer les changements et fermer la connexion
            connection.commit()
            connection.close()
            print("Modèle de bouteille ajouté avec succès.")

class Bouteille:
    def __init__(self ,nom_etagere, name, note_perso, qt_totale):
        self.nom_etagere = nom_etagere
        self.name = name
        self.note_perso = note_perso
        self.qt_totale = qt_totale
        instance1 = Etagere(nom_etagere)
        self.id_etagere = instance1.get_id_etagere(nom_etagere)

    def ajouter_bouteille(self):

        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

       # Vérifier si l'étagère a suffisamment de place
        cursor.execute("SELECT nb_bouteille_dispo, nb_bouteille FROM Etagere WHERE id_etagere=?", (self.id_etagere,))
        etagere_info = cursor.fetchone()
        print(etagere_info)

        if etagere_info[0] > 0:  # S'il y a de la place dans l'étagère
            # Demander à l'utilisateur les caractéristiques du modèle de bouteille
            name = input("Nom du vin: ")
            domaine = input("Domaine: ")
            type = input("Type: ")
            annee = int(input("Année: "))
            region = input("Région: ")
            commentaire = input("Commentaire: ")
            prix = int(input("Prix: "))
            note_commu = int(input("Note communauté: "))
            note_perso = int(input("Note personnelle: "))

            # Créer une instance de Bouteille avec les caractéristiques fournies par l'utilisateur
            nouveau_vin_modele = Vin(name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso)
            
            # Ajouter le modèle de bouteille dans la table Bouteille
            nouveau_vin_modele.ajouter_vin()

            # Récupère l'id du modele
            cursor.execute("SELECT id_vin FROM Vin WHERE name=? AND domaine=? AND type=? AND annee=? AND region=? AND commentaire=? AND prix=? AND note_commu=? AND note_perso=?",
                            (name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso))
            id_modele_vin = cursor.fetchone()
            id_modele_vin = id_modele_vin[0]

            # Vérifier si la bouteille existe déjà dans MesBouteilles
            cursor.execute("SELECT id_bouteille, qt_totale FROM Bouteille "
                           "WHERE id_vin=? AND id_etagere=?",
                           (id_modele_vin, self.id_etagere))
            existing_bouteille = cursor.fetchone()

            if existing_bouteille:
                # Si la bouteille existe déjà, augmenter la quantité de 1
                new_quantity = existing_bouteille[1] + 1
                cursor.execute("UPDATE Bouteille SET qt_totale=? WHERE id_bouteille=?",
                               (new_quantity, existing_bouteille[0]))
                print("Bouteille ajoutée avec succès. Nouvelle quantité:", new_quantity)
                connection.commit()
                connection.close()

            else:
                # Sinon, ajouter la bouteille dans MesBouteilles
                cursor.execute("INSERT INTO Bouteille (id_vin, id_etagere, name, note_perso, qt_totale)"
                               " VALUES (?, ?, ?, ?, ?)",
                               (id_modele_vin, self.id_etagere, self.name, self.note_perso, 1))
                connection.commit()
                
                print("la bouteille a vraiment été ajouté")
                # Réduire nb_bouteille_dispo de 1 et augmenter nb_bouteille de 1 dans l'étagère
                cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?",
                               (etagere_info[0] - 1, etagere_info[1] + 1, self.id_etagere))
                connection.commit()
                connection.close()

                print("Bouteille ajoutée avec succès.")
        else:
            print("L'étagère est pleine. Impossible d'ajouter la bouteille.")

    
    def supprimer_bouteille(self, id_MaBouteille):
         # Établir une connexion à la base de données
            connection = sqlite3.connect('bouteille.db')
            cursor = connection.cursor()

            # Vérifier si la bouteille existe dans MesBouteilles et récupère le nombre d'exemplaire
            cursor.execute("SELECT id_bouteille, qt_totale FROM Bouteille "
                           "WHERE id_bouteille=? AND id_etagere=?",
                           (id_MaBouteille, self.id_etagere))
            existing_bouteille = cursor.fetchone()

            if existing_bouteille:
                if existing_bouteille[1] > 1:
                    # Si la quantité est supérieure à 1, réduire la quantité de 1
                    new_quantity = existing_bouteille[1] - 1
                    cursor.execute("UPDATE Bouteille SET qt_totale=? WHERE id_bouteille=?",
                                   (new_quantity, existing_bouteille[0]))
                    print("Bouteille supprimée avec succès. Nouvelle quantité:", new_quantity)
                    connection.commit()
                    connection.close()

                else:
                    # Si la quantité est égale à 1, supprimer la bouteille de MesBouteilles
                    print(existing_bouteille[0])
                    cursor.execute("DELETE FROM Bouteille WHERE id_bouteille=?", (existing_bouteille[0],))
                    print("Bouteille supprimée avec succès.")
                    connection.commit()
                    connection.close()

            else:
                print("Bouteille non trouvée.")
        # Ajouter la logique pour supprimer une bouteille de la table MesBouteilles
        # Si la quantité est supérieure à 1, réduire la quantité de 1
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
    
# Exemple d'utilisation
# Création d'une instance de la classe Bouteille
Nouveau_vin = Vin(
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
#Nouveau_vin.ajouter_vin()

# bouteille1.ajouter_modele_bouteille()

# mes_bouteilles1 = Bouteille("etagere_1", "david", 10, 1)
# mes_bouteilles1.ajouter_bouteille()
# mes_bouteilles1.ajouter_bouteille()
#mes_bouteilles1.supprimer_bouteille(4)

#test etagere
nv_etagere = Etagere("etagere_1")
nv_etagere.ajouter_etagere(id_user=5, id_cave=1, nb_bouteille=0, nb_bouteille_dispo=15)
# nv_etagere.liste_bouteilles()

#test user
user1 = User("john", "motdepasse123")
user1.ajouter_user()
# user1.authentification_user()
# user1.supprimer_user()




