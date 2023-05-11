from flask import render_template, redirect, request
from app import app

#importe les classes Patient, RH et Archives
from modules.resident import Patient, RH
from modules.administration import Archive
from utils import enlever_espace_debut_fin, today_str

import mysql.connector as mysqlpy

def get_db_connection():
    user = 'root'
    password = 'example'
    host = 'localhost'
    port = '3308'
    database = 'CHU_caen'
    bdd = mysqlpy.connect(user=user, password=password, host=host, port=port, database=database)
    return bdd

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#page d'accueil
@app.route('/')
def init():
    return render_template('accueil.html', title='Accueil')

#tableau des patients
@app.route('/patients')
def patients():
    bdd = get_db_connection()
    cursor = bdd.cursor()

    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    
    #systématiquement qu'une fonction fait appel à la base de données, 'bdd' est envoyé comme argument
    #j'ai préféré laisser la fonction get_db_connection dans ce fichier pour pour ne pas faire appel à 'mysql.connector' ailleur que dans le fichier 'routes'
    count = Patient.count_patients_in_db(bdd)

    bdd.close()
    cursor.close()

    return render_template('patients.html', title='Nos patients', patients=patients, count = count)

#ajoute un patient à 'patients' et 'archives' avec la date du jour par défaut pour l'arrivée
@app.route('/patient-ajouter', methods=['GET', 'POST'])
def patients_ajouter():
    if request.method == 'POST':
        bdd = get_db_connection()   

        #utilise la fonction enlever_espace_debut_fin pour enlever les espaces en début et fin pour éviter de futurs erreurs losqu'il faudra comparer pour modifier ou supprimer
        nom = enlever_espace_debut_fin(request.form['nom'])
        prenom = enlever_espace_debut_fin(request.form['prenom'])
        groupe_sanguin = enlever_espace_debut_fin(request.form['groupe-sanguin'])
        identifiant_patient = nom + prenom + groupe_sanguin + today_str + '-p'

        Patient.entrer_a_l_hopital(bdd, identifiant_patient, nom, prenom, groupe_sanguin)
        Archive.enregister_en_base(bdd, identifiant_patient)
        
        bdd.close()

        return redirect('patients')
    return render_template('patients-ajouter.html', title='ajouter patient')

#supprime un patient dans 'patients' et précise la date de sortie (par défaut, date du jour) dans 'archive'
@app.route('/patient-supprimer', methods=['GET', 'POST'])
def patients_supprimer():
    if request.method == 'POST':
        bdd = get_db_connection()       

        identifiant_patient = enlever_espace_debut_fin(request.form['id-patient'])

        Patient.sortir_de_l_hopital(bdd, identifiant_patient)
       
        bdd.close()

        return redirect('patients')
    return render_template('patients-supprimer.html', title='supprimer patient')

 #tableau des ressources humaines
@app.route('/rh')
def rh():
    bdd = get_db_connection()
    cursor = bdd.cursor()

    cursor.execute('SELECT * FROM rh')
    rh = cursor.fetchall()

    bdd.close()
    cursor.close()
    return render_template('rh.html', title='rh', rh=rh)

#ajoute un collaborateur à 'rh' et 'archives' avec la date du jour par défaut pour l'arrivée
@app.route('/rh-ajouter', methods=['GET', 'POST'])
def rh_ajouter():
    if request.method == 'POST':
        bdd = get_db_connection()   

        nom = enlever_espace_debut_fin(request.form['nom'])
        prenom = enlever_espace_debut_fin(request.form['prenom'])
        salaire = enlever_espace_debut_fin(request.form['salaire'])
        identifiant_rh = nom + prenom + salaire +today_str+'-rh'

        RH.debuter_CDD_CDI(bdd, identifiant_rh, nom, prenom, salaire)
        Archive.enregister_en_base(bdd, identifiant_rh)
        
        bdd.close()

        return redirect('rh')
    return render_template('rh-ajouter.html', title='rh ajouter')

#supprime un collaborateur dans 'rh' et précise la date de sortie (par défaut, date du jour) dans 'archive'
@app.route('/rh-supprimer', methods=['GET', 'POST'])
def rh_supprimer():
    if request.method == 'POST':
        bdd = get_db_connection()       

        identifiant_rh = enlever_espace_debut_fin(request.form['id-rh'])

        RH.quitter_CDD_CDI(bdd, identifiant_rh)
       
        bdd.close()

        return redirect('rh')
    return render_template('rh-supprimer.html', title='rh supprimer')

#tableau archives des entrées et sortis des patients et collaborateurs 
@app.route('/archive')
def archive():
    bdd = get_db_connection()

    archives = Archive.afficher_les_archives(bdd)

    Archive.afficher_les_archives_console(bdd)

    bdd.close()

    return render_template('archive.html', title='archives', archives=archives)

#rajouter/modifier la date de sortie d'un patient/collaborateur avec son identifiant_resident
@app.route('/sortie', methods=['GET', 'POST'])
def sortie():
    if request.method == 'POST':
        bdd = get_db_connection()
        
        identifiant_resident = enlever_espace_debut_fin(request.form['id-resident'])
        date_sortie = enlever_espace_debut_fin(request.form['date-sortie'])

        Archive.date_de_sortie(bdd, identifiant_resident, date_sortie)

    return render_template('archive-sortie.html', title='archives modification')

#ajoute un ou plusieurs résidents, à la fois, dans la table 'archive' et les tables 'patients' et 'rh'
@app.route('/aleatoire-resident', methods=['GET', 'POST'])
def aleatoire_resident():
    if request.method == 'POST':
        bdd = get_db_connection()

        #nombre de résidents qui doit être généré
        number = int(request.form['aleatoire'])

        Archive.créer_un_resident(bdd, number, today_str)

        return redirect('archive')
    
    return render_template('aléatoire-resident.html')


