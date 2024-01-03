import sqlite3
from models.etagere import Etagere
from models.vin import Vin

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
    
    def afficher_bouteille(self):

        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = """
            SELECT 
                B.id_bouteille,
                V.id_vin,
                V.name AS vin_name,
                V.damaine,
                V.type,
                V.annee,
                V.region,
                V.commentaire AS vin_commentaire,
                V.prix,
                V.note_commu,
                V.note_perso AS vin_note_perso,
                B.name AS bouteille_name,
                B.note_perso AS bouteille_note_perso,
                B.qt_totale
            FROM Bouteille B
            JOIN Vin V ON B.id_vin = V.id_vin
            WHERE B.id_etagere = :id_etagere;
        """

        # Exécution de la requête avec le paramètre :id_etagere
        cursor.execute(query, {"id_etagere": self.id_etagere})
        
        # Récupération de tous les résultats
        result = cursor.fetchall()

        print (result)


