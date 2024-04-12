from functools import wraps
from flask import Flask, render_template, request, redirect, session, Response,url_for, abort
import json
import datamodel as model
from CreateDb import *
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


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.get("/profil")
def get_profil():
    return render_template('profil.html')

@app.route('/')
def index():
    session['auth_success']=False
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
        session['auth_success']=True
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
    skills=model.skills
    interests=model.interests
    print(interests)
    # Rechercher les bénévoles correspondant au nom
    matching_volunteers = search_volunteer_by_name(search_query)
    print("Résultats de la recherche :", matching_volunteers)
    
    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultat.html', volunteers=matching_volunteers, interests=interests,skills=skills)


@app.route('/search1')
def search_volunteers_by_location():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_volunteersf = search_volunteer_by_location_keyword(search_query)
    print("Résultats de la recherche :", matching_volunteersf)


    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultat.html', volunteers=matching_volunteersf, interests=model.interests,skills=model.skills)







@app.route('/filtrer')
def filtrer():

    skills = request.args.get('skills')
    print(skills)
    interests = request.args.get('interests')
    print(interests)
    sexe = request.args.get('sexe')
    print(sexe)
    age = request.args.get('age')
    print(age)
    

    volunteers = search_volunteers_by_filter(skills=skills, interests=interests, sexe=sexe, age=age)
    for volunteer in volunteers:
     print(volunteer)
    return render_template('resultat.html', volunteers=volunteers, interests=model.interests, skills=model.skills)





@app.route('/searchpro')
def search_projects():
    search_query = request.args.get('name', '')
    matching_projects = search_project_by_keyword(search_query)
    print("Résultats de la recherche :", matching_projects)
    print(len(matching_projects))
    return render_template('resultatProjet.html', projects=matching_projects,size=len(matching_projects))


@app.route('/searchpro2')
def search_projects_by_location():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_projectsf = search_project_by_location_keyword(search_query)
    print("Résultats de la recherche :", matching_projectsf)
    print(len(matching_projectsf))

    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultatProjet.html', projects=matching_projectsf, interests=model.interests,skills=model.skills,size=len(matching_projectsf))




@app.route('/searchpro3')
def search_projects_by_period_route():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    matching_projectsr=search_projects_by_period(start_date,end_date)
    print( matching_projectsr)
    return render_template('resultatProjet.html', projects=matching_projectsr, size=len(matching_projectsr))


    
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
