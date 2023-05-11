import random
from datetime import datetime, date

#supprime les espaces au début et à la fin pour éviter les erreurs lors de la reconnaissance dans la bdd
def enlever_espace_debut_fin(str):
    return str.strip()

#renvoie le service auquel appartiendra le résident
def patient_ou_collab():
    resident = ''
    p_ou_c = random.randint(0, 1)
    if p_ou_c == 0:
        resident = '-p'
        return resident
    elif p_ou_c == 1:
        resident = '-rh'
        return resident

#renvoie le groupe sanguin généré aléatoirement parmi les 8 possibilitées
def generer_groupe_sanguin():
    groupe_sanguin = ''
    list_groupe_sanguin = ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
    index = random.randint(0, 7)
    groupe_sanguin = list_groupe_sanguin[index]
    return groupe_sanguin

#renvoie le salaire généré aléatoirement compris entre 1.000 et 10.000 compris
def generer_salaire():
    random_salaire = random.randint(1000, 100000)
    return random_salaire

#fonction de mise à jour des sorties résident dans les tables patients et rh par rapport à la dernière lettre de l'identifiant
def mise_a_jour_date_sortie(bdd, identifiant_resident, date_sortie):
    cursor = bdd.cursor()
    cursor.execute(f'''UPDATE archives SET date_sortie= {date_sortie} WHERE identifiant_resident = "{identifiant_resident}";''')
    bdd.commit()

    if identifiant_resident[-1] == 'p':
        cursor.execute(f'''UPDATE patients SET is_in_hospital = 0 WHERE identifiant_patient="{identifiant_resident}";''')
        bdd.commit()
    elif identifiant_resident[-1] == 'h':
        cursor.execute(f'''UPDATE rh SET working_at_hospital = 0 WHERE identifiant_rh="{identifiant_resident}";''')
        bdd.commit()

    cursor.close()

#met la date en format jourMoisAnnée en le prenant que la date sans l'heure
def format_dateAAAAMMJJ(date):
    return datetime.strptime(date, "%Y-%m-%d").date()

#rajoute la date du jour pour l'identifiant_patient avec le format JourMoisAnnnée
today_str = str(date.today().strftime("%d%m%Y"))
    