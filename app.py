from flask import Flask, render_template, request, redirect
import json
import datamodel as model
import math

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
