from flask import Flask, render_template, request, redirect, url_for, render_template_string
import random, re, json, uuid
from utilities import read_todo_file, run_validations, invalid_form_template, delete_todo_from_file

app = Flask(__name__)
todo_list = read_todo_file()

@app.route('/')

def index():
    """
    The index route for the todo app. 

    Parameters: None

    Returns: The index template.
    """
    return render_template('index.html', todo_list=todo_list, cache_bust=random.random())


@app.route('/submit', methods=['POST'])
def submit():
    """
    The submit route for the todo app

    Parameters: form values of task, email and priority

    Returns: The index.html or an error screen if a input is missing.
    """
    form_values = request.form
    dict_form_values = dict(form_values)
    uuid_dict = {'uuid': str(uuid.uuid1())}
    validations = run_validations(dict_form_values)
  
    if('Incorrect' in validations.values()):
        return render_template_string(invalid_form_template(), form=validations)

    todo_list.append({**dict_form_values, **uuid_dict})

    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    """
    The clear route for the todo app

    Parameters: None

    Returns: clear's the todo object and returns the index.html.
    """
    with open('todo-list.json', 'w') as file:
        json.dump([], file)
    
    todo_list.clear()

    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save():
    """
    The save route for the todo app

    Parameters: None

    Returns: Saves the todo object into a json format and returns the index.html.
    """
    with open('todo-list.json', 'w') as file:
        json.dump(todo_list, file)

    return redirect(url_for('index'))


@app.route('/delete/<uuid>')
def delete(uuid):
    """
    The delete route for the todo app

    Parameters: UUID identifying the todo

    Returns: deletes the todo from the todo object and json file, also returns the index.html.
    """
    todo = None

    for todo_item in todo_list:
        if todo_item['uuid'] == uuid:
            todo = todo_item

    if todo in todo_list:
        todo_list.remove(todo)

    delete_todo_from_file(todo)    

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    todo_list = read_todo_file()