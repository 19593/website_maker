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
    print(results)
    return render_template("/biceps_chart.html", data = [['Date', 'Circumference']] + results )

@app.route('/graph_thigh')
def graph_thigh():
    cursor = get_db().cursor()
    sql = 'SELECT Week, Thigh FROM Thigh'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("/thigh_chart.html", data = [['Date', 'Circumference']] + results )

@app.route('/graph_uarm')
def graph_uarm():
    cursor = get_db().cursor()
    sql = 'SELECT Week, Uarm FROM Uarm'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template("/uarm_chart.html", data = [['Date', 'Circumference']] + results )

@app.route('/graph_calve')
def graph_calve():
    cursor = get_db().cursor()
    sql = 'SELECT Week, Calve FROM Calve'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template("/calve_chart.html", data = [['Date', 'Circumference']] + results )



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()





#redirections

#to chart list
@app.route('/go_to_chart', methods=['GET','POST'])
def go_to_charts():
    return redirect('/chart')

#to homepage
@app.route('/go_to_homepage', methods=['GET','POST'])
def go_to_homepage():
    return redirect('/')

#to graph_biceps
@app.route('/go_to_graph_biceps', methods=['GET','POST'])
def go_to_graph_biceps():
    return redirect('/graph_biceps')

#to graph_thigh
@app.route('/go_to_graph_thigh', methods=['GET','POST'])
def go_to_graph_thigh():
    return redirect('/graph_thigh')

#to graph_uarm
@app.route('/go_to_graph_uarm', methods=['GET','POST'])
def go_to_graph_uarm():
    return redirect('/graph_uarm')

#to graph_uarm
@app.route('/go_to_graph_calve', methods=['GET','POST'])
def go_to_graph_calve():
    return redirect('/graph_calve')

#to full_measurement
@app.route('/go_to_full_measurement', methods=['GET','POST'])
def go_to_full_measurement():
    return redirect('/full_measurement')

#to table thigh
@app.route('/go_to_table_thigh', methods=['GET','POST'])
def go_to_table_thigh():
    return redirect('/table_thigh')

#to table biceps
@app.route('/go_to_table_biceps', methods=['GET','POST'])
def go_to_table_biceps():
    return redirect('/table_biceps')

#to table uarm
@app.route('/go_to_table_uarm', methods=['GET','POST'])
def go_to_table_uarm():
    return redirect('/table_uarm')

#to table calve
@app.route('/go_to_table_calve', methods=['GET','POST'])
def go_to_table_calve():
    return redirect('/table_calve')

#redirections





#homepage
@app.route('/', methods=['GET','POST'])
def home():                                              #                   |
    cursor = get_db().cursor()                           #Big SQL Statement \ /<        Union Thigh                             Union Calce                             Union Uarm
    sql = 'SELECT Week, AVG(Biceps) AS avg_Biceps FROM (SELECT Week, Biceps FROM Biceps UNION ALL SELECT Week, Thigh FROM Thigh UNION ALL SELECT Week, Calve FROM Calve UNION ALL SELECT Week, Uarm FROM Uarm)t GROUP BY Week HAVING COUNT(*) = 4 ORDER BY Week' 
    cursor.execute(sql)
    results = cursor.fetchall()
    sql1 = 'SELECT Week, Biceps FROM Biceps' 
    cursor.execute(sql1)
    results1 = cursor.fetchall()
    return render_template('homepage.html', data = [['Date', 'Circumference']] + results, data1 = [['Date', 'Circumference']] + results1 )

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




#TABLE UARM

@app.route('/table_uarm')
def table_uarm():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Uarm'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Uarm_table.html', results=results)

#add to table uram
@app.route('/add_uarm', methods=['GET','POST'])
def add_uarm():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_uarm = request.form['item_uarm']
        new_week = request.form['item_week']
        sql = 'INSERT INTO Uarm(Week,Uarm) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_uarm))
        get_db().commit()
    return redirect('/table_uarm')

#delete from table uram
@app.route('/delete_uarm', methods=['GET','POST'])
def delete_uarm():
    if request.method == 'POST':
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM Uarm WHERE Week=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/table_uarm")

#TABLE Calve

@app.route('/table_calve')
def table_calve():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Calve'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('calve_table.html', results=results)

#add to calve(calve)
@app.route('/add_calve', methods=['GET','POST'])
def add_calve():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_calve = request.form['item_calve']
        new_week = request.form['item_week']
        sql = 'INSERT INTO Calve(Week,Calve) VALUES(?,?)'
        cursor.execute(sql,(new_week,new_calve))
        get_db().commit()
    return redirect('/table_calve')

#delete from table calve
@app.route('/delete_calve', methods=['GET','POST'])
def delete_calve():
    if request.method == 'POST':
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM Calve WHERE Week=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect("/table_calve")





if __name__== '__main__':
    app.run(debug=True)