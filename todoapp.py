from flask import Flask, render_template, request, redirect, url_for, render_template_string
import random, re

app = Flask(__name__)

@app.route('/')
def index():
    todo_list =  [
        {'id': 1, 'task': 'get cheese', 'email': 'bluecheesee123@gmail.com', 'priority': 'Hard'},
        {'id': 2, 'task': 'get milk', 'email': 'cable@gmail.com', 'priority': 'Low'},
        {'id': 3, 'task': 'take out trash', 'email': 'ce123@gmail.com', 'priority': 'Medium'}
    ]
    
    return render_template('index.html', todo_list=todo_list, cache_bust=random.random())

@app.route('/submit', methods=['POST'])
def submit():
    form_values = request.form
    dict_form_values = dict(form_values)
    validations = run_validations(dict_form_values)
    
    if('Incorrect' in validations.values()):
        return render_template_string(invalid_form_values(), form=validations)

    return redirect(url_for('index'))

def invalid_form_values():
    return"""
    <h2>Please correct the following incorrect fields:</h2>
        <div>
            <span>Task:</span>
            <span>{{form.task}}</span>
        </div>
        <div>
            <span>Email:</span>
            <span>{{form.email}}</span>
        </div>
        <div>
            <span>Priority</span>
            <span>{{form.priority}}</span>
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