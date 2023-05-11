"""
Hello !

L'equipe est très heureuse de t'accueillir dans nos rangs !
Comme convenu je te laisse corriger dans les plus brefs détails corriger la débâcle du stagiaire.

Tu as ci-dessous les attributs & methodes à intégrer dans les classes Archive, Patient et RH .

Je te rappelle que les classes Archives se situent dans modules/administration.py
et Patient & RH dans modules/resident

Je te laisse également consulter les notes des RH qui t'expliquent précisemment ce qu'elles veulent
comme fonctionalités !

Bon courage !

PG

ps : N'oublie pas de bien commenter ton code ! ;)

"""


# Archives ##########################
""" Les attributs :

identifiant_resident
date_entree 	
date_sortie 

"""

def enregister_archive_en_base():
    pass

@staticmethod
def afficher_les_archives_console():
    pass

@staticmethod
def afficher_les_archives_streamlit():
    pass


# Patient ###########################
""" Les attributs :

identifiant_patient (= nom + prenom + groupe sanguin + date de recrutement)
nom 
prenom
groupe_sanguin
is_in_hospital (True si entrer_a_l_hopital, False si sortir_de_l_hopital)

"""

def entrer_a_l_hopital():
    pass

def sortir_de_l_hopital():
    pass


# RH ################################

""" Les attributs :

identifiant_rh 	(= nom + prenom + groupe sanguin + date d'entrée)
nom 	
prenom 	
salaire 	
working_at_hospital (True si debuter_CDD_CDI, False si quitter_CDD_CDI)


"""
def debuter_CDD_CDI():
    pass

def quitter_CDD_CDI():
    pass