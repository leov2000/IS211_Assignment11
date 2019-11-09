from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

@app.route('/')
def index():
    todo_list =  [
        {'id': 1, 'task': 'get cheese', 'email': 'bluecheesee123@gmail.com', 'priority': 'Hard'},
        {'id': 2, 'task': 'get milk', 'email': 'cable@gmail.com', 'priority': 'Low'},
        {'id': 3, 'task': 'take out trash', 'email': 'ce123@gmail.com', 'priority': 'Medium'}
    ]
    
    return render_template('index.html', todo_list=todo_list, cache_bust=random.random())

if __name__ == '__main__':
    app.run()