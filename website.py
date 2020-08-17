from flask import Flask,g,render_template,request,redirect
import datetime
import sqlite3


app = Flask(__name__)


DATABASE = 'Improve.db'


#functions


#get_db

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db








#full_measurement
@app.route('/full_measurement', methods=['GET','POST'])
def full_measurement():
    cursor = get_db().cursor()
    # sql = 'SELECT Biceps.Week, average_measurement = AVG(Biceps.Biceps, Thigh.Thigh) FROM Biceps INNER JOIN Thigh ON Biceps.Week = Thigh.Week' WORAFDAWSFASFDASDFASDFASDFASDFASDFASDFASDFASD
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template('/full_measurement.html', data = [['Date', 'Circumference']] + results )

@app.route('/add_full_measurement', methods=['GET','POST'])
def add_full_measurement():
    if request.method == 'POST':
        # insert Thigh
        cursor = get_db().cursor()
        new_week = request.form['item_week']
        new_thigh = request.form['item_thigh']
        sql = 'INSERT INTO Thigh(Week,Thigh) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_thigh))

        cursor = get_db().cursor()
        new_week = request.form['item_week']
        new_biceps = request.form['item_biceps']
        sql = 'INSERT INTO Biceps(Week,Biceps) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_biceps))
        get_db().commit()
    return redirect('/full_measurement')













#graph_data
@app.route('/graph_biceps')
def graph_biceps():
    cursor = get_db().cursor()
    sql = 'SELECT Week, Biceps FROM Biceps'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("/biceps_chart.html", data = [['Date', 'Circumference']] + results )

@app.route('/graph_thigh')
def graph_thigh():
    cursor = get_db().cursor()
    sql = 'SELECT Week, Thigh FROM Thigh'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("/thigh_chart.html", data = [['Date', 'Circumference']] + results )






@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()







#redirections


#to homepage
@app.route('/go_to_homepage', methods=['GET','POST'])
def go_to_homepage():
    return redirect('/')

#to chart list
@app.route('/go_to_chart', methods=['GET','POST'])
def go_to_charts():
    return redirect('/chart')

#to graph_biceps
@app.route('/go_to_graph_biceps', methods=['GET','POST'])
def go_to_graph_biceps():
    return redirect('/graph_biceps')

#to graph_thigh
@app.route('/go_to_graph_thigh', methods=['GET','POST'])
def go_to_graph_thigh():
    return redirect('/graph_thigh')

#redirections








#homepage
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('homepage.html')

#select right table
@app.route("/tables", methods=['GET','POST'])
def tables():
    return render_template("tables.html")

#select right chart
@app.route("/chart", methods=['GET','POST'])
def chart():
    return render_template("/chart.html")



























#TABLES


#TABLE THIGH

@app.route('/table_thigh')
def table_thigh():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Thigh'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Thigh_table.html', results=results)

#add to table(thigh)
@app.route('/add_thigh', methods=['GET','POST'])
def add_thigh():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_thigh = request.form['item_thigh']
        new_week = request.form['item_week']
        sql = 'INSERT INTO Thigh(Week,Thigh) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_thigh))
        get_db().commit()
    return redirect('/table_thigh')

#delete from table thigh
@app.route('/delete_thigh', methods=['GET','POST'])
def delete_thigh():
    if request.method == 'POST':
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM Thigh WHERE Week=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/table_thigh")




#TABLE BICEPS

@app.route('/table_biceps')
def table_biceps():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Biceps'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Biceps_table.html', results=results)

#add to table biceps
@app.route('/add_biceps', methods=['GET','POST'])
def add_biceps():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_biceps = request.form['item_biceps']
        new_week = request.form['item_week']
        sql = 'INSERT INTO Biceps(Week,Biceps) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_biceps))
        get_db().commit()
    return redirect('/table_biceps')

#delete from table biceps
@app.route('/delete_biceps', methods=['GET','POST'])
def delete_biceps():
    if request.method == 'POST':
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM Biceps WHERE Week=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/table_biceps")









   

if __name__== '__main__':
    app.run(debug=True)