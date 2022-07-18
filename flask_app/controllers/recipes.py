from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Recipe import Recipe


@app.route('/create')
def create_recipe():
    return render_template ("new_recipe.html",  user = User.get_by_id(session))

@app.route('/new_recipe', methods=["POST"])
def new_recipe():
    if len(request.form['name'])<2 or len(request.form['description'])<2 or len(request.form['instructions'])<2:
        flash('All fields must have atleast 3 characters!', 'recipe')
        return redirect('/create')
    new_recipe = {
        "name":request.form['name'],
        "description":request.form['description'],
        "instructions":request.form['instructions'],
        "under_30":request.form['under_30'],
        "made_on":request.form['made_on'],
        "user_id":session['user_id']
    }
    Recipe.save(new_recipe)
    return redirect ('/dashboard')

@app.route('/show_recipe/<int:id>/')
def view_recipe(id):
    recipe = Recipe.get_by_id_with_creator(id)
    return render_template("show_recipe.html", recipe = recipe, user = User.get_by_id(session))

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if not session['user_id'] == Recipe.get_by_id_with_creator(id).user_id:
        return redirect('/dashboard')
    recipe = Recipe.get_by_id_with_creator(id)
    return render_template('edit_recipe.html', recipe = recipe, user = User.get_by_id(session))

@app.route('/update_recipe/<int:id>', methods=['POST'])
def update_recipe(id):
    updated_recipe = {
        "id":request.form['id'],
        "name":request.form['name'],
        "description":request.form['description'],
        "instructions":request.form['instructions'],
        "under_30":request.form['under_30'],
        "made_on":request.form['made_on'],
        "user_id":session['user_id']
    }
    Recipe.update_recipe(updated_recipe)
    return redirect(f'/show_recipe/{id}')