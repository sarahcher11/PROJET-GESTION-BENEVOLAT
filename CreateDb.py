import sqlite3
import json
from werkzeug.security import generate_password_hash


JSONFILENAME = 'users.json'
DBFILENAME = 'Data.sqlite'

def db_run(query, args=(),db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur= conn.execute(query,args)
    conn.execute
   

def load(fname=JSONFILENAME, db_name=DBFILENAME):
  # possible improvement: do whole thing as a single transaction
  db_run('DROP TABLE IF EXISTS user')
  db_run('DROP TABLE IF EXISTS volunteer')
  db_run('DROP TABLE IF EXISTS project_manager')
  db_run('DROP TABLE IF EXISTS project_registration')
  db_run('DROP TABLE IF EXISTS project')

  db_run('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, registration_date TEXT)')
 
  insert1 = 'INSERT INTO user VALUES (:id,:username, :password, :email, :registration_date)'
  


  with open('users.json', 'r') as fh:
     users = json.load(fh)
  for id, user in enumerate(users):
    user['id'] = id
    db_run(insert1, user)
  

def add_user(username,password,email):
  insert = 'INSERT INTO user (username,password,email) VALUES (?, ?, ?)'
  password_hash=generate_password_hash(password)
  db_run(insert,(username,password_hash,email))

load()
add_user("sarah","12345",'sarah@exemple.com')
add_user("ines","hamiche",'ines@gmail.com')
add_user("souso","azerty",'soso@gmail.com')


