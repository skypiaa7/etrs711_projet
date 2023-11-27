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
    def __init__(self ,id_etagere, column_name, note_perso, qt_totale):
        self.id_etagere = id_etagere
        self.column_name = column_name
        self.note_perso = note_perso
        self.qt_totale = qt_totale

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
            nouvelle_bouteille_modele = Bouteille(name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso)
            
            # Ajouter le modèle de bouteille dans la table Bouteille
            nouvelle_bouteille_modele.ajouter_modele_bouteille()

            # Récupère l'id du modele
            cursor.execute("SELECT id_bouteille FROM Bouteille WHERE name=? AND domaine=? AND type=? AND annee=? AND region=? AND commentaire=? AND prix=? AND note_commu=? AND note_perso=?",
                            (name, domaine, type, annee, region, commentaire, prix, note_commu, note_perso))
            id_modele_bouteille = cursor.fetchone()
            id_modele_bouteille = id_modele_bouteille[0]

            # Vérifier si la bouteille existe déjà dans MesBouteilles
            cursor.execute("SELECT id_mesbouteilles, qt_totale FROM MesBouteilles "
                           "WHERE id_bouteille=? AND id_etagere=?",
                           (id_modele_bouteille, self.id_etagere))
            existing_mesbouteille = cursor.fetchone()

            if existing_mesbouteille:
                # Si la bouteille existe déjà, augmenter la quantité de 1
                new_quantity = existing_mesbouteille[1] + 1
                cursor.execute("UPDATE MesBouteilles SET qt_totale=? WHERE id_mesbouteilles=?",
                               (new_quantity, existing_mesbouteille[0]))
                print("Bouteille ajoutée avec succès. Nouvelle quantité:", new_quantity)
                connection.commit()

            else:
                # Sinon, ajouter la bouteille dans MesBouteilles
                cursor.execute("INSERT INTO MesBouteilles (id_bouteille, id_etagere, column_name, note_perso, qt_totale)"
                               " VALUES (?, ?, ?, ?, ?)",
                               (id_modele_bouteille, self.id_etagere, self.column_name, self.note_perso, 1))
                connection.commit()
                
                print("la bouteille a vraiment été ajouté")
                # Réduire nb_bouteille_dispo de 1 et augmenter nb_bouteille de 1 dans l'étagère
                cursor.execute("UPDATE Etagere SET nb_bouteille_dispo=?, nb_bouteille=? WHERE id_etagere=?",
                               (etagere_info[0] - 1, etagere_info[1] + 1, self.id_etagere))
                connection.commit()

                print("Bouteille ajoutée avec succès.")
        else:
            print("L'étagère est pleine. Impossible d'ajouter la bouteille.")

    
    def supprimer_bouteille(self, id_MaBouteille):
         # Établir une connexion à la base de données
            connection = sqlite3.connect('votre_base_de_donnees.db')
            cursor = connection.cursor()

            # Vérifier si la bouteille existe dans MesBouteilles et récupère le nombre d'exemplaire
            cursor.execute("SELECT id_mesbouteilles, qt_totale FROM MesBouteilles "
                           "WHERE id_mesbouteilles=? AND id_etagere=?",
                           (id_MaBouteille, self.id_etagere))
            existing_mesbouteille = cursor.fetchone()

            if existing_mesbouteille:
                if existing_mesbouteille[1] > 1:
                    # Si la quantité est supérieure à 1, réduire la quantité de 1
                    new_quantity = existing_mesbouteille[1] - 1
                    cursor.execute("UPDATE MesBouteilles SET qt_totale=? WHERE id_mesbouteilles=?",
                                   (new_quantity, existing_mesbouteille[0]))
                    print("Bouteille supprimée avec succès. Nouvelle quantité:", new_quantity)
                else:
                    # Si la quantité est égale à 1, supprimer la bouteille de MesBouteilles
                    cursor.execute("DELETE FROM MesBouteilles WHERE id_mesbouteilles=?", (existing_mesbouteille[0],))
                    print("Bouteille supprimée avec succès.")

            else:
                print("Bouteille non trouvée dans MesBouteilles.")
        # Ajouter la logique pour supprimer une bouteille de la table MesBouteilles
        # Si la quantité est supérieure à 1, réduire la quantité de 1
        

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

mes_bouteilles1 = MesBouteilles(1, "david", 10, 1)
mes_bouteilles1.ajouter_bouteille()
# mes_bouteilles1.supprimer_bouteille()