from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.data.session_items import *

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items(), lists=get_lists())

@app.route('/addItem', methods = ['POST'])
def add_todo_item():
    add_item(request.form.get('name'), request.form.get('description'))
    return redirect('/')

@app.route('/complete/<id>/<list>', methods = ['POST'])
def complete_todo_item(id, list):
    save_item(id, list)
    return redirect('/')

@app.route('/delete/<id>', methods = ['DELETE'])
def delete_todo_item(id):
    delete_item(str(id))
    return '', 200

if __name__ == '__main__':
    app.run()
