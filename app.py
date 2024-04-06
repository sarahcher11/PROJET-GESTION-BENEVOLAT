from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load data from JSON file
with open('data.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/loginn')
def signup():
    return render_template('signup.html')

@app.route('/inscrProjectManager')
def inscrProjectManager():
    return render_template('inscrProjectManager.html')

@app.route('/registerVolunteer')
def registerVolunteer():
    return render_template('registerVolunteer.html')





# Route for search functionality
@app.route('/search')
def search_benevoles():
    # Get search query from request parameters
    search_query = request.args.get('q', '').lower()
    
    # List to store matching volunteers
    matching_benevoles = []

    # Search for matching volunteers
    for benevole in data['benevoles']:
        # Make search case-insensitive
        if search_query in benevole['nom'].lower() or any(interest.lower() == search_query for interest in benevole['interets']):
            matching_benevoles.append(benevole)
    
    # Render template with matching volunteers
    return render_template('resultats.html', benevoles=matching_benevoles)





if __name__ == '__main__':
    app.run(debug=True)
