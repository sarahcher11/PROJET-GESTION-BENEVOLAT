import sqlite3
import json
from datetime import datetime



JSONFILENAMEUSER = 'users.json'
JSONFILENAMEVOLUNTEER = 'volunteer.json'
DBFILENAME = 'Data.sqlite'

def db_run(query, args=(),db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur= conn.execute(query,args)
    conn.execute
   

def load_users(fname=JSONFILENAMEUSER, db_name=DBFILENAME):
  # possible improvement: do whole thing as a single transaction
  db_run('DROP TABLE IF EXISTS user')
  db_run('DROP TABLE IF EXISTS volunteer')
  db_run('DROP TABLE IF EXISTS project_manager')
  db_run('DROP TABLE IF EXISTS project_registration')
  db_run('DROP TABLE IF EXISTS project')

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

    # Créer la table volunteer
    db_run('''CREATE TABLE volunteer (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 full_name TEXT,
                 date_of_birth TEXT,
                 address TEXT,
                 skills TEXT,
                 phone_number TEXT,
                 sexe TEXT,
                 interests TEXT
              )''')

    insert_query = 'INSERT INTO volunteer (user_id, full_name, date_of_birth, address, skills, phone_number, sexe, interests) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'


    with open(fname, 'r') as fh:
        volunteers = json.load(fh)

    # Convertir les dates de naissance en format "YYYY-MM-DD"
    for volunteer in volunteers:
        volunteer['date_of_birth'] = datetime.strptime(volunteer['date_of_birth'], '%Y-%m-%d').strftime('%Y-%m-%d')

    # Préparer les données à insérer sous forme de liste de tuples
    data_to_insert = [(volunteer['user_id'], volunteer['full_name'], volunteer['date_of_birth'], volunteer['address'],
                       ', '.join(volunteer['skills']), volunteer['phone_number'], volunteer['sexe'],
                       ', '.join(volunteer['interests'])) for volunteer in volunteers]

    
    with sqlite3.connect(db_name) as conn:
            conn.executemany(insert_query, data_to_insert)









def add_volunteer(user_id, full_name, date_of_birth, address, skills, phone_number, sexe, interests, db_name=DBFILENAME):
    insert_query = '''INSERT INTO volunteer (user_id, full_name, date_of_birth, address, skills, phone_number, sexe, interests)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    # Convertir la liste de compétences et d'intérêts en chaînes de caractères séparées par des virgules
    skills_str = ', '.join(skills)
    interests_str = ', '.join(interests)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (user_id, full_name, date_of_birth, address, skills_str, phone_number, sexe, interests_str))
            conn.commit()
            volunteer_id = cursor.lastrowid 
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout du volontaire à la base de données:", e)
        return None
    
    # Mettre à jour le fichier JSON
    volunteer_data = {
        "id": volunteer_id,
        "user_id": user_id,
        "full_name": full_name,
        "date_of_birth": date_of_birth,
        "address": address,
        "skills": skills,
        "phone_number": phone_number,
        "sexe": sexe,
        "interests": interests
    }
    
    try:
        with open(JSONFILENAMEVOLUNTEER, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append(volunteer_data)
    
    with open(JSONFILENAMEVOLUNTEER, 'w') as file:
        json.dump(data, file, indent=4)
    
    return volunteer_id



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

#test
load_users()
load_volunteers()

def search_volunteer_by_name(name, db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer WHERE full_name LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + name + '%',))
            matching_volunteers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche du bénévole dans la base de données:", e)
        return None
    
    return matching_volunteers



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






































