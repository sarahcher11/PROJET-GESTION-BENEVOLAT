from functools import wraps
from flask import Flask, render_template, request, redirect, session, Response,url_for, abort
import json
import datamodel as model
from CreateDb import *
from CreateDb import search_volunteer_by_name
import math
from flask import request, jsonify
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
from email.mime.text import MIMEText
import base64
 
app = Flask(__name__)
app.secret_key = 'gghyednejcn'

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_credential.json'



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
def inscrProjectManager():
    if 'user_id' in session:
        return render_template('inscrProjectManager.html')
    else :
        return render_template('HomePage.html', erreur="you should connect first to your account")

@app.get('/registerVolunteer')
def registerVolunteer():
     if 'user_id' in session:
         return render_template('registerVolunteer.html',interests=model.interests,skills=model.skills)
     else :
          return render_template('HomePage.html', erreur="you should connect first to your account")




@app.post('/login')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user_id = model.login(email, password)
    if user_id != -1:
        session['user_id']=user_id
        session['auth_success']=True
        current_user=model.get_user_by_id(user_id)
        session['username']=current_user[1]
        session['email']=current_user[3]
        session['img']=model.get_image(user_id)
        return redirect('/login')
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
        session['username']=username
        session['email']=email
        session['auth_success']=True
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
    return render_template('resultatbenevole.html', volunteers=matching_volunteers, interests=interests,skills=skills)


@app.route('/search1')
def search_volunteers_by_location():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_volunteersf = search_volunteer_by_location_keyword(search_query)
    print("Résultats de la recherche :", matching_volunteersf)


    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultatbenevole.html', volunteers=matching_volunteersf, interests=model.interests,skills=model.skills)







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
    return render_template('resultatbenevole.html', volunteers=volunteers, interests=model.interests, skills=model.skills)





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
    
    id=model.add_volunteer(session['user_id'],first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code,
                        skills_selectionnes, phone_number, gender, interests_selectionnes)
    session['volunteer_id']=id
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
    model.add_project_manager(session['user_id'],first_name, last_name, date_of_birth, address, address_line2, country, city, region, postal_code, phone_number, gender)
    return redirect('/')


@app.post('/changepwd')
def change_password():
    current_password=request.form['current_password']
    new_password=request.form['new_password']
    new_password_cf=request.form['new_password_cf']
    if model.check_password( session['user_id'],current_password):
        if new_password == new_password_cf:
            model.change_password(session['user_id'],new_password)
            return redirect("/")
        else :
            erreur= 'Passwords do not match. Please try again'
            return render_template('profil.html', error=erreur)
    else :
        erreur ="You've entered a wrong current password."
        return render_template('profil.html', error=erreur)

@app.get('/addProject')
def add_project():
     return render_template("projectform.html",interests=model.interests)

@app.post('/addProject')
def add_project_form():
    project_name = request.form['project_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    address = request.form['address']
    city = request.form['city']
    postal_code = request.form['postal_code']
    region = request.form['region']
    interests = json.loads(request.form['interests'])
    description = request.form['description']
    project_manager=model.search_manager_by_userid(session['user_id'])
    model.add_project(project_name,description,start_date,end_date,region,city,postal_code,address,project_manager[0],interests)
    return render_template('myProjects.html',projet_cree='true')


@app.get('/myprojects')
def display_projects():
     id=session['user_id']
     project_manager=model.search_manager_by_userid(id)
     if project_manager!=None :
         projects=model.get_projets_with_id(project_manager[0])
         return render_template('myProjects.html',projects=projects )
     else :
        return render_template('HomePage.html',erreur2="you are not a project manager")

@app.get('/contact/<int:id>')
def contact_volunteer(id):
    volunteer=model.get_volunteer_by_id(id)
    print(volunteer)
    user=model.get_user_by_id(volunteer[1])
    print(user)
    return render_template("sendmail.html",destinataire=user[3])






def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)



def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server()
    return credentials

def send_email(sender, to, subject, message):
    credentials = get_credentials()
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

    message = create_message(sender, to, subject, message)
    send_message(service, "me", message)

@app.post("/contact")
def contact_form():
    if request.method == 'POST':
        sender = session['email'] 
        recipient = request.form['recipient']  
        subject = request.form['subject']  
        body = request.form['message']  

        send_email(sender, recipient, subject, body)
        return  render_template("sendmail.html",sent='true')
    else:
        return jsonify({"message": "Method not allowed"}), 405




if __name__ == '__main__':
    app.run(debug=True)
