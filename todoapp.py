from flask import Flask, render_template, request, redirect, url_for, render_template_string
import random, re, json

app = Flask(__name__)

@app.route('/')
def index():
    todo_list = read_todo_file()
    
    return render_template('index.html', todo_list=todo_list, cache_bust=random.random())

@app.route('/submit', methods=['POST'])
def submit():
    form_values = request.form
    dict_form_values = dict(form_values)
    validations = run_validations(dict_form_values)
  
    if('Incorrect' in validations.values()):
        return render_template_string(invalid_form_template(), form=validations)
    
    write_to_file(dict_form_values)

    return redirect(url_for('index'))

def write_to_file(form_values):
    todo_list = read_todo_file()
    append_value = [*todo_list, form_values]

    with open('todo-list.json', 'w') as file:
        json.dump(append_value, file)

def read_todo_file():
    try:
        todo_list = json.loads(open('todo-list.json').read())

    except IOError:
        with open('todo-list.json', 'w') as file:
            json.dump([], file)
        
        todo_list = json.loads(open('todo-list.json').read())

    return todo_list 

def invalid_form_template():
    return"""
    <h2>Please correct the following incorrect fields:</h2>
        <div>
            <span>Task:</span>
            <span {% if form.task == 'Incorrect' %} style="color:red;" {% endif %}>{{form.task}}</span>
        </div>
        <div>
            <span>Email:</span>
            <span {% if form.email == 'Incorrect' %} style="color:red;" {% endif %}>{{form.email}}</span>
        </div>
        <div>
            <span>Priority</span>
            <span {% if form.priority == 'Incorrect' %} style="color:red;" {% endif %}>{{form.priority}}</span>
        </div>
    """

def validations_config():
    return {
        'task': lambda task: 'Correct' if task else 'Incorrect',
        'email': lambda email: 'Correct' if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email) else 'Incorrect',
        'priority':  lambda p: 'Correct' if p.lower() == 'low' or p.lower() == 'hard' or p.lower() == 'medium' else 'Incorrect'
    }    

def run_validations(form_dict):
    validations = validations_config()

    return dict([(k, validations[k](v)) for k, v in form_dict.items()])  

if __name__ == '__main__':
    app.run()