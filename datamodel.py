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



"""Lire le contenu d'une recette à partir de son identifiant.

Cette fonction prend en argument un identifiant de recette.

Elle renvoie une recette sous la forme d'un objet :
- title: son titre
- description: la description textuelle de la recette
- duration: la durée totale de la recette
- img: l'url de son image
- ingredients: une liste d'ingrédients (pour chacun il y a un champ name)
- stages: une liste d'étapes pour la recette (chacune contient un champ description)

Cette fonction renvoie None si l'identifiant n'existe pas.
"""
def read(id):
  found = db_fetch('SELECT * FROM user WHERE id = ?', (id,))
  if (not(found is None)):
    found['ingredients'] = db_fetch('SELECT name FROM ingredient WHERE recipe = ? ORDER BY rank',
                                    (id,), all=True)
    found['stages'] = db_fetch('SELECT description FROM stage WHERE recipe = ? ORDER BY rank',
                               (id,), all=True)
  return found


"""Fonction pour créer une nouvelle recette dans la base.

Prend en paramètre un objet python décrivant la recette sous la forme suivante :
recipe = {
  title: 'text',
  description: 'text',
  duration: 'text',
  ingredients: [
    {name: 'text'},
    ...
  ],
  stages: [
    {description: 'text'},
    ...
  ]
}

Cette fonction retourne l'identifiant de la recette créée.

Possible improvement: create the whole recipe as a single transaction.
"""
def create(recipe):
  id = db_insert('INSERT INTO recipe (title, img, description, duration) VALUES (:title, :img, :description, :duration)',
                 recipe)
  ingredients, stages = recipe['ingredients'], recipe['stages']
  for r, ingredient in enumerate(ingredients):
    db_run('INSERT INTO ingredient VALUES (:recipe, :rank, :name)',
           {'recipe': id, 'rank': r, 'name': ingredient})
  for r, stage in enumerate(stages):
    db_run('INSERT INTO stage VALUES (:recipe, :rank, :description)',
           {'recipe': id, 'rank': r, 'description': stage})
  return id

"""Fonction pour mettre à jour une recette de la base.

Un identifiant de recette doit être passé en premier argument.
Le second argument est un objet python au même format que pour la fonction create.

Cette fonction revoie True si l'identifiant existe dans la base.

Possible improvement: update the whole recipe as a single transaction.
"""
def update(id, recipe):
  params = {key: recipe[key] for key in recipe}
  params['id'] = id
  result = db_update('UPDATE recipe SET title = :title, img = :img, description = :description WHERE id = :id',
                     params)
  if result == 1:
    ingredients, stages = recipe['ingredients'], recipe['stages']
    db_run('DELETE FROM ingredient WHERE recipe = ?', (id,))
    for r, ingredient in enumerate(ingredients):
      db_run('INSERT INTO ingredient VALUES (:recipe, :rank, :name)',
             {'recipe': id, 'rank': r, 'name': ingredient})
    db_run('DELETE FROM stage WHERE recipe = ?', (id,))
    for r, stage in enumerate(stages):
      db_run('INSERT INTO stage VALUES (:recipe, :rank, :description)',
             {'recipe': id, 'rank': r, 'description': stage})
    return True
  else:
    return False


"""Fonction pour effacer une recette dans la base à partir de son identifiant"""
def delete(id):
  db_run('DELETE FROM recipe WHERE id = ?', (id,))
  db_run('DELETE FROM ingredient WHERE recipe = ?', (id,))
  db_run('DELETE FROM stage WHERE recipe = ?', (id,))

""" Recherche d'une recette par requête, avec pagination des résultats

Cette fonction prend en argument la requête sous forme d'une chaîne de caractères
et le numéro de la page de résultats.

Cette fonction retourne un dictionnaire contenant les champs suivants :
- results: liste de recettes (version courte contenant l'identifiant de la recette, son titre et l'url de son image)
- num_found: le nombre de recettes trouvées
- query: la requête
- next_page: numero de la page suivante
- page: numero de la page courante
- num_pages: nombre total de pages
"""
def search(query="", page=1):
  num_per_page = 32
  # on utiliser l'opérateur SQL LIKE pour rechercher dans le titre 
  res = db_fetch('SELECT count(*) FROM recipe WHERE title LIKE ?',
                       ('%' + query + '%',))
  num_found = res['count(*)']
  results = db_fetch('SELECT id as entry, title, img FROM recipe WHERE title LIKE ? ORDER BY id LIMIT ? OFFSET ?',
                     ('%' + query + '%', num_per_page, (page - 1) * num_per_page), all=True)
  return {
    'results': results,
    'num_found': num_found, 
    'query': query,
    'next_page': page + 1,
    'page': page,
    'num_pages': math.ceil(float(num_found) / float(num_per_page))
  }


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
    


def add_volunteer(first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, skills, phone_number, sexe, interests, db_name=DBFILENAME):
    global current_user_id  # Déclarez que vous utilisez la variable globale current_user_id

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
    print(interests_str)
    print(skills_str)
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


def add_project_manager(first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, phone_number, sexe, db_name=DBFILENAME):
    global current_user_id  # Déclarez que vous utilisez la variable globale current_user_id

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
    

def get_user_by_id(user_id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM user WHERE id=?'''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (user_id,))
            result = cursor.fetchone()  # Fetches the first row
            if result:
                return result  # Returns the entire row as a tuple
            else:
                print("Aucun utilisateur trouvé avec l'ID:", user_id)
                return None
    except sqlite3.Error as e:
        print("Erreur lors de la récupération du nom d'utilisateur depuis la base de données:", e)
        return None




def search_manager_by_userid(user_id, db_name=DBFILENAME):
    select_query = '''SELECT * FROM project_manager WHERE user_id '''
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, ('%' + user_id + '%'))
            matching_volunteers = cursor.fetchall()
    except sqlite3.Error as e:
        print("Erreur when searching for the project manager in the data base", e)
        return None
    
    return matching_volunteers


