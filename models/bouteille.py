import sqlite3
import sys
sys.path.append('.')
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

    def ajouter_bouteille(self, name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso):

        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        # Vérifier si l'étagère a suffisamment de place
        cursor.execute("SELECT nb_bouteille_dispo, nb_bouteille FROM Etagere WHERE id_etagere=?", (self.id_etagere,))
        etagere_info = cursor.fetchone()

        if etagere_info[0] >= self.qt_totale:  # S'il y a de la place dans l'étagère
            # Créer une instance de Vin avec les caractéristiques fournies par l'utilisateur
            nouveau_vin_modele = Vin(name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso)
            
            # Ajouter le modèle de vin dans la table Vin
            nouveau_vin_modele.ajouter_vin()

            # Récupère l'id du modele
            cursor.execute("SELECT id_vin FROM Vin WHERE name=? AND domaine=? AND type=? AND annee=? AND region=? AND commentaire=? AND prix=? AND note_commu=? AND note_perso=?",
                            (name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso))
            id_modele_vin = cursor.fetchone()
            id_modele_vin = id_modele_vin[0]

            # Vérifier si la bouteille existe déjà dans Bouteille
            cursor.execute("SELECT id_bouteille, qt_totale FROM Bouteille "
                           "WHERE id_vin=? AND id_etagere=?",
                           (id_modele_vin, self.id_etagere))
            existing_bouteille = cursor.fetchone()

            if existing_bouteille:
                # Si la bouteille existe déjà, augmenter la quantité de 1
                new_quantity = existing_bouteille[1] + self.qt_totale
                cursor.execute("UPDATE Bouteille SET qt_totale=? WHERE id_bouteille=?",
                               (new_quantity, existing_bouteille[0]))
                connection.commit()
                cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?",
                               (etagere_info[0] - self.qt_totale, etagere_info[1] + self.qt_totale, self.id_etagere))
                connection.commit()
                connection.close()
                return True

            else:
                # Sinon, ajouter la bouteille dans Bouteille
                cursor.execute("INSERT INTO Bouteille (id_vin, id_etagere, name, note_perso, qt_totale)"
                               " VALUES (?, ?, ?, ?, ?)",
                               (id_modele_vin, self.id_etagere, self.name, self.note_perso, self.qt_totale))
                connection.commit()
                
                # Réduire nb_bouteille_dispo de 1 et augmenter nb_bouteille de 1 dans l'étagère
                cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?",
                               (etagere_info[0] - self.qt_totale, etagere_info[1] + self.qt_totale, self.id_etagere))
                connection.commit()
                connection.close()

                return True
        else:
            return None

    
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
    
ma_bouteille = Bouteille("etagere_3", "Bouteille1", 8, 2)

# Appeler la méthode ajouter_bouteille avec des paramètres de test
# result = ma_bouteille.ajouter_bouteille("Vin1", "Domaine1", "Type1", 2000, "Region1", "Commentaire1", 20, 7, 8)

# Vérifier le résultat
# if result is None:
#     print("L'étagère est pleine. Impossible d'ajouter la bouteille.")
# elif result is True:
#     print("Bouteille ajoutée avec succès.")
# else:
#     print("Une erreur s'est produite.")



