from functools import wraps
from flask import Flask, render_template, request, redirect, session, Response,url_for, abort
import json
import datamodel as model
from CreateDb import search_volunteer_by_name
import math
 
app = Flask(__name__)
app.secret_key = 'gghyednejcn'


def login_required(f):
  @wraps(f)
  def decorated_function(*args,**kwargs):
    if 'user_id' not in session :
      return Response('Unauthorized', 401)
    return f(*args,**kwargs)
  return decorated_function




@app.route('/')
def index():
    return render_template('HomePage.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.get('/inscrProjectManager')
@login_required
def inscrProjectManager():
    return render_template('inscrProjectManager.html')

@app.get('/registerVolunteer')
@login_required
def registerVolunteer():
    return render_template('registerVolunteer.html',interests=model.interests,skills=model.skills)

@app.post('/login')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user_id = model.login(email, password)
    if user_id != -1:
        session['user_id']=user_id
        return redirect('/')
    else:
        erreur = 'Failed authentification'
        return render_template("login.html", error=erreur)

@app.post('/signup')
def new_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    user_id = model.new_user(email, password, username)

    if user_id!=None:
        session['user_id']=user_id
        return redirect('/')
    else:
        erreur = 'Already existing email or username'
        return render_template("signup.html", error=erreur)


@app.route('/search')
def search_volunteers():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_volunteers = search_volunteer_by_name(search_query)
    print("Résultats de la recherche :", matching_volunteers)


    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultat.html', volunteers=matching_volunteers)




@app.post('/registerVolunteer')
def register_volunteer_form():
    first_name = request.form['first_name']
    last_name = request.form["last_name"]
    phone_number = request.form['phone_number']
    date_of_birth = request.form['date_of_birth']
    gender = request.form.get('gender')
    address = request.form["address"]
    address_line2 = request.form['address_line2']
    country = request.form.get('country')
    city = request.form['city']
    region = request.form['region']
    postal_code = request.form['postal_code']
    
    # Décoder les listes JSON en structures de données Python
    interests_selectionnes = json.loads(request.form['interests'])
    skills_selectionnes = json.loads(request.form['skills'])
    
    for interest in interests_selectionnes:
        print(interest)
    
    model.add_volunteer(first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code,
                        skills_selectionnes, phone_number, gender, interests_selectionnes)
    return redirect('/')


@app.post("/inscrProjectManager")
def register_form_manager():
    first_name = request.form['first_name']
    last_name = request.form["last_name"]
    phone_number = request.form['phone_number']
    date_of_birth = request.form['date_of_birth']
    gender = request.form.get('gender')
    address = request.form["address"]
    address_line2 = request.form['address_line2']
    country = request.form.get('country')
    city = request.form['city']
    region = request.form['region']
    postal_code = request.form['postal_code']
    model.add_project_manager(first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, phone_number, gender)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
