import sqlite3
import json
from datetime import datetime


JSONFILENAMEUSER = 'users.json'
JSONFILENAMEVOLUNTEER = 'volunteer.json'
JSONFILENAMEMANAGER = 'manager.json'
DBFILENAME = 'Data.sqlite'

def db_run(query, args=(),db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur= conn.execute(query,args)
    conn.execute
   

def load_users(fname=JSONFILENAMEUSER, db_name=DBFILENAME):
  # possible improvement: do whole thing as a single transaction
  db_run('DROP TABLE IF EXISTS user')


  #la table user 
  db_run('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, registration_date TEXT)')
  insert1 = 'INSERT INTO user VALUES (:id,:username, :password, :email, :registration_date)'
  with open('users.json', 'r') as fh:
     users = json.load(fh)
  for id, user in enumerate(users):
    user['id'] = id
    db_run(insert1, user)




def load_volunteers(fname=JSONFILENAMEVOLUNTEER, db_name=DBFILENAME):
    # Supprimer la table volunteer s'il existe déjà
    db_run('DROP TABLE IF EXISTS volunteer')

    # Créer la table volunteer avec les nouvelles colonnes
    db_run('''CREATE TABLE volunteer (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 first_name TEXT,
                 last_name TEXT,
                 date_of_birth TEXT,
                 address TEXT,
                 adress_line2 TEXT,
                 country TEXT,
                 city TEXT,
                 region TEXT,
                 post_code TEXT,
                 skills TEXT,
                 phone_number TEXT,
                 sexe TEXT,
                 interests TEXT
              )''')

    insert_query = 'INSERT INTO volunteer (user_id, first_name, last_name, date_of_birth, address, adress_line2, country, city, region, post_code, skills, phone_number, sexe, interests) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    with open(fname, 'r') as fh:
        volunteers = json.load(fh)

    # Convertir les dates de naissance en format "YYYY-MM-DD"
    for volunteer in volunteers:
        volunteer['date_of_birth'] = datetime.strptime(volunteer['date_of_birth'], '%Y-%m-%d').strftime('%Y-%m-%d')

        # Convertir les compétences en une chaîne de caractères séparée par des virgules
        volunteer['skills'] = ', '.join(volunteer['skills'])

        # Convertir les intérêts en une chaîne de caractères séparée par des virgules
        volunteer['interests'] = ', '.join(volunteer['interests'])

    # Préparer les données à insérer sous forme de liste de tuples
    data_to_insert = [(volunteer['user_id'], volunteer['first_name'], volunteer['last_name'], volunteer['date_of_birth'], volunteer['address'],
                       volunteer['adress_line2'], volunteer['country'], volunteer['city'], volunteer['region'], volunteer['post_code'],
                       volunteer['skills'], volunteer['phone_number'], volunteer['sexe'], volunteer['interests']) for volunteer in volunteers]

    with sqlite3.connect(db_name) as conn:
        conn.executemany(insert_query, data_to_insert)

def load_projectmanagers(fname=JSONFILENAMEMANAGER, db_name=DBFILENAME):
    # Supprimer la table volunteer s'il existe déjà
    db_run('DROP TABLE IF EXISTS project_manager')

    # Créer la table volunteer avec les nouvelles colonnes
    db_run('''CREATE TABLE project_manager (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 first_name TEXT,
                 last_name TEXT,
                 date_of_birth TEXT,
                 address TEXT,
                 adress_line2 TEXT,
                 country TEXT,
                 city TEXT,
                 region TEXT,
                 post_code TEXT,
                 phone_number TEXT,
                 sexe TEXT
              )''')

    insert_query = 'INSERT INTO  project_manager(user_id, first_name, last_name, date_of_birth, address, adress_line2, country, city, region, post_code, phone_number, sexe) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    with open(fname, 'r') as fh:
       managers = json.load(fh)

    # Convertir les dates de naissance en format "YYYY-MM-DD"
    for manager in managers:
        manager['date_of_birth'] = datetime.strptime(manager['date_of_birth'], '%Y-%m-%d').strftime('%Y-%m-%d')

      

    # Préparer les données à insérer sous forme de liste de tuples
    data_to_insert = [(manager['user_id'], manager['first_name'], manager['last_name'], manager['date_of_birth'], manager['address'],
                       manager['adress_line2'], manager['country'], manager['city'], manager['region'], manager['post_code'],
                        manager['phone_number'], manager['sexe']) for manager in managers]

    with sqlite3.connect(db_name) as conn:
        conn.executemany(insert_query, data_to_insert)



def get_volunteers(db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            volunteers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la récupération des bénévoles depuis la base de données:", e)
        return None
    
    return volunteers



def search_volunteer_by_name(name, db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer WHERE first_name LIKE ? OR last_name LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + name + '%','%' + name + '%'))
            matching_volunteers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche du bénévole dans la base de données:", e)
        return None
    
    return matching_volunteers

load_projectmanagers()
load_volunteers()
'''
#Test get_volunteers
volunteers = get_volunteers()
if volunteers:
    print("Liste des bénévoles disponibles:")
    for volunteer in volunteers:
        print(volunteer)
else:
    print("Erreur lors de la récupération des bénévoles.")



#Test search_volunteer_by_name
search_name = "so"
volunteer = search_volunteer_by_name(search_name)
if volunteer:
    print(f"Bénévole trouvé avec le nom '{search_name}': {volunteer}")
else:
    print(f"Aucun bénévole trouvé avec le nom '{search_name}'.")

'''




































