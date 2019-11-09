import json, re

def read_todo_file():
    try:
        todo_list = json.loads(open('todo-list.json').read())

    except IOError:
        todo_list = []

    return todo_list

def delete_todo_from_file(todo):
    try:
        json_list = json.loads(open('todo-list.json').read())

    except IOError:
        json_list = False

    if json_list and todo in json_list:
        json_list.remove(todo)

        with open('todo-list.json', 'w') as file:
            json.dump(json_list, file)

def validations_config():
    return {
        'task': lambda task: 'Correct' if task else 'Incorrect',
        'email': lambda email: 'Correct' if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email) else 'Incorrect',
        'priority':  lambda p: 'Correct' if p.lower() == 'low' or p.lower() == 'hard' or p.lower() == 'medium' else 'Incorrect'
    }    

def run_validations(form_dict):
    validations = validations_config()

    return dict([(k, validations[k](v)) for k, v in form_dict.items()])

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