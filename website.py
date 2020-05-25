from flask import Flask,g,render_template,request,redirect
import sqlite3

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
        new_bicepse = request.form['item_bicepse']
        sql = 'INSERT INTO contents(Bicepse) VALUES(?)'
        cursor.execute(sql,(new_bicepse))
        get_db().commit()
    return redirect('/')









   

if __name__== '__main__':
    app.run(debug=True)