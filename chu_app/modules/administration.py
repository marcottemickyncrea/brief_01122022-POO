from flask import flash, redirect

# utiliser d'une API randomuser pour générer des patients aléatoirement.
from randomuser import RandomUser

from utils import patient_ou_collab, generer_groupe_sanguin, generer_salaire, mise_a_jour_date_sortie, format_dateAAAAMMJJ

class Archive:
    #enregistre le patient/résident dans archive dès sa création avec la date de jour en entrée par défaut
    @staticmethod
    def enregister_en_base(bdd, identifiant_resident):        
        cursor = bdd.cursor()
    
        cursor.execute(f'''INSERT INTO archives (identifiant_resident, date_entree) VALUES("{identifiant_resident}", current_date);''')
        bdd.commit()

        cursor.close()

    #renvoie chaque residents dans la console dès qu'une personne se rend sur la page 'archive' pour afficher le tableau côté front
    @staticmethod
    def afficher_les_archives_console(bdd):
        cursor = bdd.cursor()
        cursor.execute('SELECT * FROM archives') 

        archives = cursor.fetchall()
        for archive in archives:
            #opération ternaire qui change la valeur 'None' lorsqu'aucune date de sortie n'est en entrée en 'non renseigné
            print(f'''{archive[0]} est entrée le {archive[1]} et sorti le {'"non renseigné"' if archive[2] == None else archive[2]}''')

    #affiche le tableau de la table 'archive'
    @staticmethod
    def afficher_les_archives(bdd):
        cursor = bdd.cursor()
        cursor.execute('SELECT * FROM archives') 

        archives = cursor.fetchall()
        return archives
    
    #met à jour la date de sortie en prenant en compte si c'est un patient ou un collaborateur(rh)
    @staticmethod
    def date_de_sortie(bdd, identifiant_resident, date_sortie):
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT date_entree FROM archives WHERE identifiant_resident = "{identifiant_resident}";''')
        date_entree = cursor.fetchone()            
            
        #si aucune date de sortie n'est entrée dans le formulaire, la date du jour est entrée par défaut dans la table 'archives'
        #et modifie les valeurs de présence dans les tables 'patients' et 'rh'
        if date_sortie == '':
            date_sortie = 'current_date'
            #'mise_a_jour_date_sortie' se situe dans utils, car je l'utilise deux fois dans des conditions différentes dans la même fonction
            mise_a_jour_date_sortie(bdd, identifiant_resident, date_sortie)
            #redirect apparait ici, mais ne fonctionne pas !? Je l'ai placé ici pour éviter une redirection lorsque la date de sortie est mauvaise
            return redirect('archive')
        #si la date de sortie se situe avant la date d'entrée, renvoie une erreur via flash
        elif date_entree[0] > format_dateAAAAMMJJ(date_sortie):
            flash(f'''Votre date de sortie {format_dateAAAAMMJJ(date_sortie)} se situe après la date d'entrée !''')   
        #si la date de sortie se situe pareil ou après alors mise des infos dans la table 'archives'
        #et modifie les valeurs de présence dans les tables 'patients' et 'rh'
        elif date_entree[0] <= format_dateAAAAMMJJ(date_sortie):
            date_sortie = f'''"{format_dateAAAAMMJJ(date_sortie)}"'''
            mise_a_jour_date_sortie(bdd, identifiant_resident, date_sortie)
            #idem
            return redirect('archive')
    
    #permet de créer un ou plusieurs nouveaux résidents
    @staticmethod
    def créer_un_resident(bdd, number, date_entrée):
        cursor = bdd.cursor()

        #utilisation de l'API randomuser
        #dans le cas où je n'aurais pas réussi, j'aurais créé des tableaux noms et prénoms dans lequel un valeur aléatoire au pris un nom et un prénom au hasard 
        user = RandomUser()   
        #prend au compte le nombre de nouveaux résidents à générer en nationalité française pour éviter les noms utilisant un alphabet différent du latin
        user_list = RandomUser.generate_users(number, {'nat': 'fr'})
        #passe une boucle sur chaque utilisateur généré et rajoute les infos sur groupe sanguin ou salaire suivant une variable prenant 0 ou 1 pour 'patient' et 'rh'
        for user in user_list:
            #récupère le nom
            nom = user.get_last_name()
            #récupère le prénom
            prenom = user.get_first_name() 
            id_resident = nom + prenom
            info_complementaire = ''
            #utilise la fonction patient_ou_collab pour générer aléatoirement le serice auxquels ils appatiennent
            p_ou_c = patient_ou_collab()
            #les fonctions patient_ou_collab/generer_groupe_sanguin/generer_salaire ont été placé dans utils pour réduire la quantité de ligne de code dans la fonction
            #permet de générer un identifiant différent suivant le groupe dans lequel le résident est attribué
            if p_ou_c == '-p':
                info_complementaire = generer_groupe_sanguin()
                id_resident += info_complementaire
            elif p_ou_c == '-rh':
                info_complementaire = generer_salaire()
                id_resident += str(info_complementaire)
            id_resident += date_entrée + p_ou_c

            #chaque nouveaux résidents est ajouté à la table 'archive' avec la date d'arrivée du jour par défaut
            cursor.execute(f'''INSERT INTO archives (identifiant_resident, date_entree) VALUES("{id_resident}", current_date);''')
            bdd.commit()
            
            #la variable 'p_ou_c' permet de savoir dans quelle table les informations résidents doivent être ajouté
            if p_ou_c =='-p':
                cursor.execute(f'''INSERT INTO patients VALUES("{id_resident}", "{nom}", "{prenom}", "{info_complementaire}", 1);''')
                bdd.commit()
            elif p_ou_c ==  '-rh':
                cursor.execute(f'''INSERT INTO rh VALUES("{id_resident}", "{nom}", "{prenom}", "{info_complementaire}", 1);''')
                bdd.commit()

    