import sqlite3 

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return self.name is not None and self.password is not None
    
    @staticmethod
    def get_by_id(user_id):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM User WHERE id_user = ?;
        '''
        result = cursor.execute(query, (user_id,)).fetchone()
        if result:
            user = User(result[1], result[2])
            user.id = result[0]
            return user
        else:
            return None
        connection.close()
    
    def get_id(self):
        user_id = self.get_user_id()
        if user_id is not None:
            return str(user_id)
        return None

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
            self.id = result[0]
            return True
        else:
            print("Échec de l'authentification. Nom d'utilisateur ou mot de passe incorrect.")
            return False
        connection.close()

    def is_authenticated(self):
        return self.id is not None

    def list_etagere(self):
        connection = sqlite3.connect('bouteille.db')
        cursor = connection.cursor()

        user_id = self.get_user_id()

        query = '''
            SELECT * FROM Etagere WHERE id_user = ?;
        '''
        result = cursor.execute(query, (user_id,)).fetchall()
        if result:
            print("Liste des étagères:")
            for row in result:
                print(row)
        else:
            print("Aucune étagère trouvée.")
        connection.close()

        return result
    
    