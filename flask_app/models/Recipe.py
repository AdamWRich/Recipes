from flask_app.config.mysqlconnection import connectToMYSQL
from flask import flash
from flask_app.models import User


db = "recipes"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30 = data['under_30']
        self.made_on = data['made_on']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, under_30, made_on, instructions, user_id, created_at, updated_at) VALUES ( %(name)s, %(description)s, %(under_30)s, %(made_on)s, %(instructions)s, %(user_id)s, NOW(), NOW() );"
        return connectToMYSQL(db).query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMYSQL(db).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_creator_info = {
                "id":row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" :  row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            creator = User.User(one_recipes_creator_info)
            one_recipe.creator = creator
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_by_id_with_creator(cls, id):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        data = { "id":id}
        results = connectToMYSQL(db).query_db(query, data)
        print(results)
        recipe = []
        for row in results:
            primary_recipe = cls(row)
            primary_recipe_creator_info = {
                "id":row['user_id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" :  row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            creator = User.User(primary_recipe_creator_info)
            primary_recipe.creator = creator
            recipe.append(primary_recipe)
        return recipe[0]

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30 = %(under_30)s, made_on = %(made_on)s, instructions = %(instructions)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMYSQL(db).query_db(query, data)
