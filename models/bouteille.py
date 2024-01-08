import sqlite3
import sys
sys.path.append('.')
from models.etagere import Etagere
from models.vin import Vin

class Bouteille:
    def __init__(self ,id_user, nom_etagere, name, note_perso, qt_totale):
        self.nom_etagere = nom_etagere
        self.name = name
        self.note_perso = note_perso
        self.qt_totale = qt_totale
        instance1 = Etagere(nom_etagere, id_user)
        self.id_etagere = instance1.get_id_etagere()

    def ajouter_bouteille(self, name, domaine, type, annee, region, commentaire, prix, note_commu):

        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()
        
        # Vérifier si l'étagère a suffisamment de place
        cursor.execute("SELECT nb_bouteille_dispo, nb_bouteille FROM Etagere WHERE id_etagere=?", (self.id_etagere,))
        etagere_info = cursor.fetchone()
            
        if etagere_info is None:
            return False
        
        else:
            if etagere_info[0] >= self.qt_totale:  # S'il y a de la place dans l'étagère
                # Créer une instance de Vin avec les caractéristiques fournies par l'utilisateur
                nouveau_vin_modele = Vin(name, domaine, type, annee, region, commentaire, prix, note_commu)
                
                # Ajouter le modèle de vin dans la table Vin
                nouveau_vin_modele.ajouter_vin()

                # Récupère l'id du modele
                cursor.execute("SELECT id_Vin FROM Vin WHERE name=? AND domaine=? AND type=? AND annee=? AND region=? AND commentaire=? AND prix=? AND note_commu=?",
                                (name, domaine, type, annee, region, commentaire, prix, note_commu))
                id_modele_vin = cursor.fetchone()
                result = id_modele_vin[0]
                print(result)

                # Vérifier si la bouteille existe déjà dans Bouteille
                cursor.execute("SELECT id_bouteille, qt_totale FROM Bouteille "
                            "WHERE id_vin=? AND id_etagere=?",
                            (result, self.id_etagere))
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
                                (result, self.id_etagere, self.name, self.note_perso, self.qt_totale))
                    connection.commit()
                    
                    # Réduire nb_bouteille_dispo de 1 et augmenter nb_bouteille de 1 dans l'étagère
                    cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?",
                                (etagere_info[0] - self.qt_totale, etagere_info[1] + self.qt_totale, self.id_etagere))
                    connection.commit()
                    connection.close()

                    return True
            else:
                return None

    
    def supprimer_bouteille(self, id_MaBouteille, qt_suppr, id_etagere):
         # Établir une connexion à la base de données
            connection = sqlite3.connect('bouteille.db')
            cursor = connection.cursor()

            # Vérifier si la bouteille existe dans MesBouteilles et récupère le nombre d'exemplaire
            cursor.execute("""
                SELECT B.id_bouteille, E.nb_bouteille, E.nb_bouteille_dispo, B.qt_totale 
                FROM Bouteille B
                JOIN Etagere E ON B.id_etagere = E.id_etagere
                WHERE B.id_bouteille=? AND B.id_etagere=?
            """, (id_MaBouteille, id_etagere))
            existing_bouteille = cursor.fetchone()

            if existing_bouteille:
            
                if existing_bouteille[1] > qt_suppr:
                    # Si la quantité est supérieure à 1, réduire la quantité de 1
                    new_quantity = existing_bouteille[1] - qt_suppr
                    new_nb_bouteille_dispo = existing_bouteille[2] + qt_suppr
                    new_nb_bouteille = existing_bouteille[3] - qt_suppr
                    cursor.execute("UPDATE Bouteille SET qt_totale=? WHERE id_bouteille=?",
                                   (new_quantity, existing_bouteille[0]))
                    print("Bouteille supprimée avec succès. Nouvelle quantité:", new_quantity)
                    connection.commit()
                    cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?", (new_nb_bouteille_dispo, new_nb_bouteille, id_etagere))
                    connection.commit()
                    connection.close()
                    return True

                else:
                    # Si la quantité est égale à 1, supprimer la bouteille de MesBouteilles
                    print(existing_bouteille[0])
                    cursor.execute("DELETE FROM Bouteille WHERE id_bouteille=?", (existing_bouteille[0],))
                    print("Bouteille supprimée avec succès.")
                    connection.commit()
                    cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?", (existing_bouteille[2] + qt_suppr, existing_bouteille[3] - qt_suppr, id_etagere))
                    connection.commit()
                    connection.close()
                    return True

            else:
                print("Bouteille non trouvée.")
                return None
    

#test fonction ajouter_bouteille
# instance = Bouteille(5, "test", "test", 1, 1)
# result = instance.ajouter_bouteille("test45", "test", "test", 1, "test", "test", 1, 1)

# if result:
#     print("Bouteille ajoutée avec succès.")
# else:
#     print("Erreur lors de l'ajout de la bouteille.")


            
