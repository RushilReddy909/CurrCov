from os import urandom
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pass"]
        con_pass = request.form["cpass"]

@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

if __name__ == "__main__":
    app.run(debug=True)