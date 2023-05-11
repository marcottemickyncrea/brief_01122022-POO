class Patient:
    #même si le code est fait, je n'utilise pas, car cela complexifierait le code
    def __init__(self, identifiant_patient, nom, prenom, groupe_sanguin):
        self.identifiant_patient = identifiant_patient
        self.nom = nom
        self.prenom = prenom
        self.groupe_sanguin = groupe_sanguin
    
    @staticmethod
    def count_patients_in_db(bdd):
        cursor = bdd.cursor()

        cursor.execute('SELECT COUNT(*) FROM patients;')
        count_patients = cursor.fetchone()

        return count_patients

    @staticmethod
    def entrer_a_l_hopital(bdd, identifiant_patient, nom, prenom, groupe_sanguin):
        cursor = bdd.cursor()
        
        #la valeur 'is_in_hospital' n'apparait pas, car sa valeur est par défaut de 1 dans la table 'patients'
        cursor.execute(f'''INSERT INTO patients (identifiant_patient, nom, prenom, groupe_sanguin) VALUES("{identifiant_patient}", "{nom}", "{prenom}", "{groupe_sanguin}");''')
        bdd.commit()       

        cursor.close()

    @staticmethod
    def sortir_de_l_hopital(bdd, identifiant_patient):
        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM patients WHERE identifiant_patient = "{identifiant_patient}";''')
        bdd.commit()
        #en même temps qu'il est suppprimé de la table 'patient', la date de sortie est mise à jour dans la table 'archive'
        cursor.execute(f'''UPDATE archives SET date_sortie = current_date WHERE identifiant_resident="{identifiant_patient}";''')
        bdd.commit()

        cursor.close()

class RH:
    @staticmethod
    def debuter_CDD_CDI(bdd, identifiant_rh, nom, prenom, salaire):
        cursor = bdd.cursor()
        
        #la valeur 'working_at_hospital' n'apparait pas, car sa valeur est par défaut de 1 dans la table 'rh
        cursor.execute(f'''INSERT INTO rh (identifiant_rh, nom, prenom, salaire) VALUES("{identifiant_rh}", "{nom}", "{prenom}", "{salaire}");''')
        bdd.commit()

        cursor.close()

    @staticmethod
    def quitter_CDD_CDI(bdd, identifiant_rh):
        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM rh WHERE identifiant_rh = "{identifiant_rh}";''')
        bdd.commit()
        
        #en même temps qu'il est suppprimé de la table 'rh', la date de sortie est mise à jour dans la table 'archive'
        cursor.execute(f'''UPDATE archives SET date_sortie =  current_date WHERE identifiant_resident = "{identifiant_rh}";''')
        bdd.commit()

        cursor.close()