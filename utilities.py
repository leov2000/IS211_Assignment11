import json, re

def read_todo_file():
    """
    A utility function that reads the json file.

    Parameters: None.

    Returns:  A list of todos or an empty list. 
    """
    try:
        todo_list = json.loads(open('todo-list.json').read())

    except IOError:
        todo_list = []

    return todo_list

def delete_todo_from_file(todo):
    """
    A utility function that reads/deletes/writes to a json file.
    
    Parameters: UUID identifying the todo.

    Returns: None
    """
    try:
        json_list = json.loads(open('todo-list.json').read())

    except IOError:
        json_list = False

    if json_list and todo in json_list:
        json_list.remove(todo)

        with open('todo-list.json', 'w') as file:
            json.dump(json_list, file)

def validations_config():
    """
    A validation utility function that checks the inputs when they're submitted.

    Parameters: None

    Returns: A validation dictionary labeled by input.
    """
    return {
        'task': lambda task: 'Correct' if task else 'Incorrect',
        'email': lambda email: 'Correct' if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email) else 'Incorrect',
        'priority':  lambda p: 'Correct' if p.lower() == 'low' or p.lower() == 'hard' or p.lower() == 'medium' else 'Incorrect'
    }    

def run_validations(form_dict):
    """
    A validation utility function that runs the validations for the inputs.

    Parameters: form values in a dictionary format

    Returns: A validation dictionary that's read by the submit route. If a incorrect value is present, the error template will be rendered.
    """
    validations = validations_config()

    return dict([(k, validations[k](v)) for k, v in form_dict.items()])

def invalid_form_template():
    """
    The invalid form template used when a value fails validation. 
    
    Returns: A HTML string.
    """
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