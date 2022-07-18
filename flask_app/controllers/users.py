import bcrypt
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Recipe import Recipe

@app.route('/')
def login_or_register():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = {
        "fname" : request.form['first_name'],
        "lname": request.form['last_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_password":request.form['confirm_password']
    }
    if not User.verify_user(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    data.pop('confirm_password')
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    print(user)
    if not user:
        flash("Invalid Email", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user[0]['password'], request.form['password']):
        flash("Invalid password", 'login')
        return redirect('/')
    session['user_id'] = user[0]['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    feed = Recipe.get_all_recipes_with_creator()
    print(feed)
    return render_template("user_dash.html", user = User.get_by_id(session), feed = feed)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
