from flask import Flask,g,render_template,request,redirect
import datetime
import sqlite3

now = datetime.datetime.now()
dateStr = now.strftime("%d-%m-%Y")


app = Flask(__name__)


DATABASE = 'Improve.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM contents'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('contents.html', results=results)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_biceps = request.form['item_biceps']
        sql = 'INSERT INTO contents(Biceps) VALUES(?)'
        cursor.execute(sql,(new_biceps,))
        get_db().commit()
    return redirect('/')


@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        cursor = get_db().cursor()









   

if __name__== '__main__':
    app.run(debug=True)