from todo_app.view_model import ViewModel
from flask import Flask, request, redirect, render_template

from todo_app.data.session_items import *
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    @app.route('/')
    def index():
        view_model = ViewModel(get_items())
        return render_template('index.html', view_model=view_model)

    @app.route('/addItem', methods = ['POST'])
    def add_todo_item():
        add_item(request.form.get('name'), request.form.get('description'))
        return redirect('/')

    @app.route('/start/<id>', methods = ['POST'])
    def start_todo_item(id):
        save_item(id, os.environ['IN_PROGRESS_LIST_ID'])
        return redirect('/')

    @app.route('/complete/<id>', methods = ['POST'])
    def complete_todo_item(id):
        save_item(id, os.environ['DONE_LIST_ID'])
        return redirect('/')

    @app.route('/reset/<id>', methods = ['POST'])
    def reset_todo_item(id):
        save_item(id, os.environ['TODO_LIST_ID'])
        return redirect('/')

    @app.route('/delete/<id>', methods = ['DELETE'])
    def delete_todo_item(id):
        delete_item(str(id))
        return '', 200

    if __name__ == '__main__':
        app.run()

    return app

