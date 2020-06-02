from flask import Flask,g,render_template,request,redirect
import datetime
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

#redirections
#to table
@app.route('/go_to_table', methods=['GET','POST'])
def go_to_table():
    return redirect('/table')

#to homepage
@app.route('/go_to_homepage', methods=['GET','POST'])
def go_to_homepage():
    return redirect('/')
#redirections

#homepage
@app.route('/')
def home():
    return render_template('homepage.html')

#table
@app.route('/table')
def table():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM contents'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('contents.html', results=results)

#add to table
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_biceps = request.form['item_biceps']
        now = datetime.datetime.now()
        dateStr = now.strftime("%d/%m/%Y")
        sql = 'INSERT INTO contents(Date,Biceps) VALUES(?,?)'
        cursor.execute(sql,(dateStr,new_biceps,))
        get_db().commit()
    return redirect('/table')

#delete from table
@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM contents WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/table")










   

if __name__== '__main__':
    app.run(debug=True)