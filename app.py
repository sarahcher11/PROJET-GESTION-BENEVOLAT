from flask import Flask, render_template, jsonify, request
from CreateDb import search_volunteer_by_name
import json

app = Flask(__name__)
'''
# Load data from JSON file
with open('data.json') as f:
    data = json.load(f)
'''


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
def inscrProjectManager():
    return render_template('inscrProjectManager.html')

@app.get('/registerVolunteer')
def registerVolunteer():
    return render_template('registerVolunteer.html')



@app.route('/search')
def search_volunteers():
    # Récupérer le terme de recherche depuis les paramètres de la requête
    search_query = request.args.get('name', '')
    
    # Rechercher les bénévoles correspondant au nom
    matching_volunteers = search_volunteer_by_name(search_query)
    print("Résultats de la recherche :", matching_volunteers)


    # Retourner les résultats de la recherche sous forme de page HTML "resultat.html"
    return render_template('resultat.html', volunteers=matching_volunteers)







if __name__ == '__main__':
    app.run(debug=True)
