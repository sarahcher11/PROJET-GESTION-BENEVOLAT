import sqlite3
import json
import os

DBFILENAME = 'app.sqlite'


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


class MoviesDB:

   def __init__(self, db_path=None):
    if db_path is not None and os.path.exists(db_path):
        self.load(db_path)
    else:
        with sqlite3.connect(DBFILENAME) as conn:
            query = '''CREATE TABLE IF NOT EXISTS movies(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            year INTEGER,
                            actors TEXT,
                            plot TEXT,
                            poster TEXT)'''
            conn.execute(query) 
            conn.commit()  


   def load(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for movie_id, movie_data in data.items():
                self.create(movie_data['title'], int(movie_data['year']), movie_data['actors'], movie_data['plot'], movie_data['poster'])

   def list(self):
        query = "SELECT * FROM movies ORDER BY id"
        result = db_fetch(query, all=True)
        if not result:
            return []
        result.sort(key=lambda e: e['id'])
        return result

   def create(self, title, year, actors, plot, poster):
        query = "INSERT INTO movies (title, year, actors, plot, poster) VALUES (?, ?, ?, ?, ?)"
        new_movie_id = db_insert(query, (title, year, actors, plot, poster))
        return new_movie_id

   def read(self, id):
        query = "SELECT * FROM movies WHERE id = ?"
        result = db_fetch(query, (id,))
        if not result:
            return None
        return result

   def update(self, id, title, year, actors, plot, poster):
        query = "UPDATE movies SET title = ?, year = ?, actors = ?, plot = ?, poster = ? WHERE id = ?"
        rows_affected = db_update(query, (title, year, actors, plot, poster, id))
        return rows_affected

   def delete(self, id):
        query = "DELETE FROM movies WHERE id = ?"
        rows_affected = db_run(query, (id,))
        return rows_affected
   def save(self, db_path):
    movie_list = db_fetch('SELECT * FROM movies ORDER BY id',
                          all=True)
    movies = {}
    for movie in movie_list:
      movies[movie['id']] = movie
    with open(db_path, 'w', encoding='utf-8') as fh:
      json.dump(movies, fh, ensure_ascii=False, indent=4)
    return True