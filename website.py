from flask import Flask
import sqlite3

app = Flask(__name__)


DATABASE = '/path/to/Improve.db'

def get_db():
    db = getattr(Flask, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return 'Hello World!'

if __name__== '__main__':
    app.run(debug=True)