from flask_app.config.mysqlconnection import connectToMYSQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "recipes"

class User:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(fname)s, %(lname)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMYSQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls, user_credentials):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        return connectToMYSQL(db).query_db(query, user_credentials)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMYSQL(db).query_db(query, data)
        print(results)
        return results[0]

    @staticmethod
    def verify_user(user):
        is_valid = True
        if user['fname'] and len(user['fname'])<2 :
            flash("First name must be at least 3 characters!", 'registration')
            print("line 31")
            is_valid = False
        if " " in user['fname'] or " " in user['lname']:
            flash("Please insert names without spaces!", 'registration')
            is_valid = False
        if user['fname'].isalpha() == False:
            flash("Please insert names without numbers!", 'registration')
        if user['lname'].isalpha() == False:
            flash("Please insert names without numbers!", 'registration')
        if user['lname'] and len(user['lname'])<2:
            flash("Last name must be at least 3 characters!", 'registration')
            is_valid = False
        if user['email'] == "":
            flash("Please insert an email!", 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']) or " " in user['email']:
            flash("Invalid email address!", 'registration')

            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMYSQL(db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", 'registration')
            print("line 49")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be 8 characters!", 'registration')
            print("line 53")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match!", 'registration')
            print("line 57")
            is_valid = False
        return is_valid
