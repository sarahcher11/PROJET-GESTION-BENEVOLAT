from flask import Flask, render_template, request, redirect
import json
import datamodel as model
from CreateDb import *
import math


app = Flask(__name__)

@app.route('/')
def index():
    volunteers=get_volunteers()
    projects=get_projects()
    return render_template('HomePage.html',totalv=len(volunteers),totalp=len(projects))

@app.get('/login')
def login():
    return render_template('login.html')


@app.get('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.get('/help')
def help():
    return render_template('help.html')

@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.get('/inscrProjectManager')
def inscrProjectManager():
    return render_template('inscrProjectManager.html')

@app.get('/registerVolunteer')
def registerVolunteer():
    return render_template('registerVolunteer.html',interests=model.interests)

@app.post('/login')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user_id = model.login(email, password)
    if user_id != -1:
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
    # Rechercher les bénévoles correspondant au nom
    matching_volunteers = search_volunteer_by_name(search_query)
    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultatbenevole.html', volunteers=matching_volunteers, interests=interests,skills=skills,size=len(matching_volunteers))


@app.route('/search1')
def search_volunteers_by_location():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_volunteersf = search_volunteer_by_location_keyword(search_query)
 


    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultatbenevole.html', volunteers=matching_volunteersf, interests=model.interests,skills=model.skills,size=len(matching_volunteersf))







@app.route('/filtrer')
def filtrer():

    skills = request.args.get('skills')
    interests = request.args.get('interests')
    sexe = request.args.get('sexe')
    age = request.args.get('age')
    

    volunteers = search_volunteers_by_filter(skills=skills, interests=interests, sexe=sexe, age=age)
    
    return render_template('resultatbenevole.html', volunteers=volunteers, interests=model.interests, skills=model.skills,size=len(volunteers))





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
    print("iiiiiiiiiiiiiiiiiiiiiiii")

    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultatProjet.html', projects=matching_projectsf,size=len(matching_projectsf))




@app.route('/searchpro3')
def search_projects_by_period_route():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    matching_projectsr=search_projects_by_period(start_date,end_date)
    print( matching_projectsr)
    return render_template('resultatProjet.html', projects=matching_projectsr, size=len(matching_projectsr))


    
@app.route('/help/envoyer_message', methods=['GET', 'POST'])
def helpp():
    if request.method == 'POST':
        # Traitement du message ici
        
        # Affichage de la fenêtre modale
        return '''
        <script>
            alert("Message envoyé avec succès !");
            window.location.href = "/";
        </script>
        '''
    else:
        return render_template('help.html')


@app.post('/registerVolunteer')
def register_volunteer_form():
    pass



if __name__ == '__main__':
    app.run(debug=True)
