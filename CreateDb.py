import sqlite3
import json
from datetime import datetime,timedelta


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

load_projectmanagers()

'''
#test
load_users()
load_volunteers()
'''

def search_volunteer_by_name(name, db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer WHERE first_name LIKE ? OR last_name LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + name + '%','%' + name + '%'))
            cursor.execute(select_query, ('%' + name + '%','%' + name + '%'))
            matching_volunteers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche du bénévole dans la base de données:", e)
        return None
    
    return matching_volunteers



def search_volunteer_by_location_keyword(keyword, db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer WHERE region LIKE ? OR city LIKE ? OR address LIKE ? OR country LIKE? OR post_code LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%','%' + keyword + '%'))
            matching_volunteerf = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche de projet dans la base de données:", e)
        return None

    return matching_volunteerf



def search_volunteers_by_filter(age=None, skills=None, sexe=None, interests=None, db_name="Data.sqlite"):
    # Connexion à la base de données
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Construction de la requête SQL
    query = "SELECT * FROM volunteer WHERE 1=1"
    parameters = []

    if age is not None:
        age = int(age)
        query += " AND DATE('now') - DATE(date_of_birth) >= ?"
        parameters.append(age)

    if skills is not None and len(skills) > 0:
        skills_conditions = skills.split(', ')
        for skill in skills_conditions:
            query += " AND skills LIKE ?"
            parameters.append('%' + skill + '%')
    if interests is not None and len(interests) > 0:
        interests_conditions = interests.split(', ')
        for interest in interests_conditions:
            query += " AND interests LIKE ?"
            parameters.append('%' + interest + '%')
    if sexe is not None:
        query += " AND sexe = ?"
        parameters.append(sexe)

    # Exécution de la requête
    cursor.execute(query, parameters)
    volunteersf = cursor.fetchall()

    # Fermeture de la connexion à la base de données
    conn.close()

    return volunteersf








def load_project_table(fname="Project.json", db_name="Data.sqlite"):
    # Supprimer la table project si elle existe déjà
    db_run('DROP TABLE IF EXISTS project')

    # Créer la table project avec les colonnes spécifiées
    db_run('''CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    description TEXT,
    start_date DATE,
    end_date DATE,
    region TEXT,
    ville TEXT,
    code_postal TEXT,
    adresse TEXT,
    project_manager_id INTEGER,
    interests TEXT
    )''')

    insert_query = '''INSERT INTO project (project_name, description, start_date, end_date, region, ville, code_postal, adresse, project_manager_id, interests)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    with open(fname, 'r') as fh:
        projects = json.load(fh)

    # Convertir les dates de début et de fin du projet en format "YYYY-MM-DD"
    for project in projects:
        project['start_date'] = datetime.strptime(project['start_date'], '%Y-%m-%d').date()
        project['end_date'] = datetime.strptime(project['end_date'], '%Y-%m-%d').date()

    # Préparer les données à insérer sous forme de liste de tuples
    data_to_insert = [(project['project_name'], project['description'], project['start_date'], project['end_date'],
                       project['region'], project['ville'], project['code_postal'], project['adresse'],
                       project['project_manager_id'], ', '.join(project['interests'])) for project in projects]

    with sqlite3.connect(db_name) as conn:
            conn.executemany(insert_query, data_to_insert)


load_project_table()
load_projectmanagers()
load_users()
load_volunteers()



def get_projects(db_name=DBFILENAME):
    select_query = '''SELECT * FROM project'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            projects = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la récupération des projets depuis la base de données:", e)
        return None
    
    return projects


def search_project_by_keyword(keyword, db_name=DBFILENAME):
    select_query = '''SELECT * FROM project WHERE project_name LIKE ? OR description LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + keyword + '%', '%' + keyword + '%'))
            matching_projects = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche de projet dans la base de données:", e)
        return None
    
    return matching_projects



matching_projects=search_project_by_keyword("programme")
print(matching_projects)

def search_project_by_location_keyword(keyword, db_name=DBFILENAME):
    select_query = '''SELECT * FROM project WHERE region LIKE ? OR ville LIKE ? OR adresse LIKE ? OR code_postal LIKE ?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
            matching_projects = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la recherche de projet dans la base de données:", e)
        return None
    
    return matching_projects






def search_projects_by_period(start_date, end_date, db_name="Data.sqlite"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = '''SELECT * FROM project 
           WHERE start_date <= ? AND end_date >= ?'''


    start_date_iso = start_date.strftime('%Y-%m-%d')
    end_date_iso = end_date.strftime('%Y-%m-%d')
    cursor.execute(query, (start_date_iso, end_date_iso))
    projects = cursor.fetchall()
    conn.close()
    return projects



start_date = datetime(2024, 5, 2)
end_date = datetime(2024, 5, 14)

# Call the function
projects = search_projects_by_period(start_date, end_date)

# Now you have a list of projects that fall within the specified period
print(projects)



























































