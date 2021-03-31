from flask import Flask, render_template, request

from todo_app.flask_config import Config
from todo_app.data.session_items import *

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/addItem', methods = ['POST'])
def addItem():
    add_item(request.form.get('name'))
    return render_template('index.html', items=get_items())

@app.route('/complete/<id>', methods = ['POST'])
def completeItem(id):
    item = get_item(id)
    item['status'] = "Complete"
    save_item(item)
    return render_template('index.html', items=get_items())


if __name__ == '__main__':
    app.run()
