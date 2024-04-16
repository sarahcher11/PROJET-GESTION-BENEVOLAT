import sqlite3
import math
from werkzeug.security import generate_password_hash, check_password_hash
import json


JSONFILENAMEUSER = 'users.json'
JSONFILENAMEVOLUNTEER = 'volunteer.json'
DBFILENAME = 'Data.sqlite'
current_user_id=None

# Liste des centres d'intérêt
interests = [
    "Music",
    "Reading",
    "Traveling",
    "Sports",
    "Cooking",
    "Art",
    "Cinema",
    "Photography",
    "Gardening",
    "Volunteering",
    "Fashion",
    "Technology",
    "Nature",
    "Animals",
    "Video Games",
    "Yoga",
    "Meditation",
    "Dance",
    "Theater",
    "Creative Writing"
]


skills = [
    "Programming",
    "Problem Solving",
    "Communication",
    "Leadership",
    "Teamwork",
    "Adaptability",
    "Time Management",
    "Decision Making",
    "Organization",
    "Creativity",
    "Critical Thinking",
    "Fast Learning",
    "Persuasion",
    "Data Analysis",
    "Stress Management",
    "Collaboration",
    "Presentation",
    "Project Management",
    "Independence",
    "Writing"
]


def db_fetch(query, args=(), all=False, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    # to allow access to columns by name in res
    conn.row_factory = sqlite3.Row 
    cur = conn.execute(query, args)
    # convert to a python dictionary for convenience
    if all:
      res = cur.fetchall()
      if res:
        res = [dict(e) for e in res]
      else:
        res = []
    else:
      res = cur.fetchone()
      if res:
        res = dict(res)
  return res

def db_insert(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.lastrowid


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()


def db_update(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.rowcount


def login(email,password):
  global current_user_id
  query='SELECT id, password FROM user WHERE email=?'
  user_data=db_fetch(query,(email,))
  if user_data:
    user_id=user_data['id']
    stored_password_hash=user_data['password']
    if check_password_hash(stored_password_hash,password):
      current_user_id=user_id
      return user_id
  return -1

def check_password(user_id, password):
    query = 'SELECT password FROM user WHERE id=?'
    user_data = db_fetch(query, (user_id,))
    print("User data:", user_data)  # Ajout d'une impression pour vérifier les données renvoyées
    if user_data and 'password' in user_data:  # Vérifiez si la clé 'password' est présente dans les données de l'utilisateur
        stored_password_hash = user_data['password']
        if check_password_hash(stored_password_hash, password):
            return True
    return False

def change_password(user_id, new_password):
    query = 'UPDATE user SET password=? WHERE id=?'
    db_run(query, (generate_password_hash(new_password), user_id))





def new_user(email, password, username):
    global current_user_id
    query_check_existence = 'SELECT id FROM user WHERE email=?'
    existing_user = db_fetch(query_check_existence, (email,))
    if existing_user:
        # L'utilisateur avec cet e-mail existe déjà, retourner None
        return None
    else:
        # L'utilisateur avec cet e-mail n'existe pas, créer un nouvel utilisateur
        password_hash = generate_password_hash(password)
        insert_query = 'INSERT INTO user (email, username, password) VALUES (?, ?, ?)'
        user_id = db_insert(insert_query, (email, username, password_hash))
        current_user_id=user_id
        return user_id
    


def add_volunteer(current_user_id,first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, skills, phone_number, sexe, interests, db_name=DBFILENAME):

    # Vérifiez si current_user_id est défini
    if current_user_id is None:
        print("current_user_id n'est pas défini. Impossible d'ajouter un volontaire.")
        return None

    # Convertir les listes de compétences et d'intérêts en chaînes de caractères séparées par des virgules et espaces
    skills_str = ""
    for skill in skills:
        skills_str += skill + ", "
    # Retirer la virgule et l'espace supplémentaires à la fin
    skills_str = skills_str[:-2]

    interests_str = ""
    for interest in interests:
        interests_str += interest + ", "
    # Retirer la virgule et l'espace supplémentaires à la fin
    interests_str = interests_str[:-2]

    insert_query = '''INSERT INTO volunteer (user_id, first_name, last_name, date_of_birth, address, adress_line2, country, city, region, post_code, skills, phone_number, sexe, interests)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (current_user_id, first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, skills_str, phone_number, sexe, interests_str))
            conn.commit()
            volunteer_id = cursor.lastrowid 
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout du volontaire à la base de données:", e)
        return None
    
    return volunteer_id


def add_project_manager(current_user_id,first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, phone_number, sexe, db_name=DBFILENAME):

    # Vérifiez si current_user_id est défini
    if current_user_id is None:
        print("current_user_id n'est pas défini. Impossible d'ajouter un volontaire.")
        return None
   
    insert_query = '''INSERT INTO project_manager (user_id, first_name, last_name, date_of_birth, address, adress_line2, country, city, region, post_code, phone_number, sexe)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (current_user_id, first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, phone_number, sexe))
            conn.commit()
            manager_id = cursor.lastrowid 
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout du volontaire à la base de données:", e)
        return None
    
    return manager_id


def get_project_manager(db_name=DBFILENAME):
    select_query = '''SELECT * FROM project_manager'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            managers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur lors de la récupération des managers depuis la base de données:", e)
        return None
    
    return managers

def get_username_for_user(user_id, db_name=DBFILENAME):
    select_query = '''SELECT username FROM user WHERE id=?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (user_id,))
            result = cursor.fetchone()  # On utilise fetchone() car nous nous attendons à un seul résultat
            if result:
                return result[0]  # Renvoie le premier (et unique) élément de la liste résultat
            else:
                print("Aucun utilisateur trouvé avec l'ID:", user_id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération du nom d'utilisateur depuis la base de données:", e)
        return None
    
def get_volunteer_by_id(id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM volunteer WHERE id=?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (id,))
            result = cursor.fetchone()  # On utilise fetchone() car nous nous attendons à un seul résultat
            if result:
                return result
            else:
                print("Aucun utilisateur trouvé avec l'ID:", id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération du nom d'utilisateur depuis la base de données:", e)
        return None



def get_projets_with_id(manager_id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM project WHERE project_manager_id=?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (manager_id,))
            result = cursor.fetchall()  
            if result:
                return result 
            else:
                print("Aucun project trouvé avec l'ID:", manager_id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération des projets depuis la base de données:", e)
        return None

projets=get_projets_with_id(1)
print(projets)

def get_user_by_id(user_id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM user WHERE id=?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (user_id,))
            result = cursor.fetchone()  # Fetches the first row
            if result:
                return result 
            else:
                print("Aucun utilisateur trouvé avec l'ID:", user_id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération du nom d'utilisateur depuis la base de données:", e)
        return None

def get_image(user_id, db_name=DBFILENAME):
    select_query = 'SELECT img FROM image WHERE user_id = ?'
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]  
            else:
                print("Aucune image trouvée pour l'utilisateur avec l'ID:", user_id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération de l'image depuis la base de données:", e)
        return None


def search_manager_by_userid(user_id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM project_manager WHERE user_id =?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ( user_id, ))
            matching_volunteers = cursor.fetchone()
    except sqlite3.Error as e:
        print("Erreur when searching for the project manager in the data base", e)
        return None
    
    return matching_volunteers


def add_project(project_name, description, start_date, end_date, region, ville, code_postal, adresse, project_manager_id, interests, db_name="Data.sqlite"):
    insert_query = '''INSERT INTO project (project_name, description, start_date, end_date, region, ville, code_postal, adresse, project_manager_id, interests)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    
    interests_str = ""
    for interest in interests:
        interests_str += interest + ", "
    # Retirer la virgule et l'espace supplémentaires à la fin
    interests_str = interests_str[:-2]
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (project_name, description, start_date, end_date, region, ville, code_postal, adresse, project_manager_id, interests_str))
            conn.commit()
            project_id = cursor.lastrowid
    except sqlite3.Error as e:
        print("Erreur lors de l'ajout du projet à la base de données:", e)
        return None

    return project_id
