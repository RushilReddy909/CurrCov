from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security
from helpers import check_email, check_pass
from datetime import timedelta
import requests
import json

app = Flask(__name__)
app.secret_key = urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours=1)

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    hash = db.Column(db.String(200))

    def __init__(self, name, email, hash):
        self.name = name
        self.email = email
        self.hash = hash
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if "u_id" not in session:
        return redirect(url_for('login'))
    else:
        response = requests.get("https://api.frankfurter.app/latest?from=INR&to=USD,EUR,JPY,GBP,AUD,CAD,CHF,CNY")
        #TODO handle error
        
        rates = response.json()["rates"]
        currencies = requests.get("https://api.frankfurter.app/currencies").json()
        return render_template('index.html', date=response.json()["date"], rates=json.dumps(rates), currencies=currencies)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if "u_id" in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template('signup.html')
    else:
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pass"]
        con_pass = request.form["cpass"]
        
        # Server Validation
        found_user = Users.query.filter_by(email = email).first()
        if not check_email(email):
            flash("Invalid Email Address provided.", "error")
            return redirect(url_for('signup'))
        
        if not check_pass(password):
            flash("Invalid Password provided.", "error")
            return redirect(url_for('signup'))
        
        if found_user:
            flash("Email already in use, please login.", "error")
            return redirect(url_for('signup'))
        
        if password != con_pass:
            flash("Passwords don't match, please try again.", "error")
            return redirect(url_for('signup'))

        # Input to Database
        hashpass = security.generate_password_hash(password)
        insert = Users(username, email, hashpass)
        db.session.add(insert)
        db.session.commit()

        flash("Registered Successfully, login to continue.", "info")
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if "u_id" in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]

        #Retrieve user from DB
        found_user = Users.query.filter_by(email = email).first()

        #Perform Validation
        if not check_email(email):
            flash("Email Address does not exist in database.", "error")
            return redirect(url_for('login'))

        if not found_user:
            flash("Account with given email does not exist.", "error")
            return redirect(url_for('login'))
        
        if not security.check_password_hash(found_user.hash, password):
            flash("Invalid Email or Password.", "error")
            return redirect(url_for('login'))
        
        #Assign session and redirect to Home Page
        session.permanent = True
        session["u_id"] = found_user.id
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if "u_id" in session:
        session.clear()
        flash("Successfully Logged out of Session.", "info")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/quote')
def quote():
    if "u_id" not in session:
        return redirect(url_for('login'))
    else:
        return render_template('quote.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)