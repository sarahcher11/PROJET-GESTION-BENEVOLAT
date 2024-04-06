import sqlite3
import json



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

    # Insérer les données des bénévoles dans la table volunteer
    for volunteer in volunteers:
        # Convertir la liste de compétences en une chaîne de caractères
        skills_str = ', '.join(volunteer['skills'])
        volunteer['skills'] = skills_str
        db_run(insert_query, volunteer)

  
load_volunteers()




