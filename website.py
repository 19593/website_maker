from flask import Flask,g,render_template,request,redirect, flash
import datetime
import sqlite3


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

DATABASE = 'Improve.db'


#functions


#get_db



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#def hasNumbers for checking if inputs have digits in them or not
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)



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

#to buy device
@app.route('/BuyDevice')
def buy_device():
    return render_template('BuyDevice.html')

#to login/register page
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

#to login page
@app.route('/login/loginn', methods=['GET','POST'])
def loginn():
    return render_template('loginn.html')

#to register page
@app.route('/login/register', methods=['GET','POST'])
def register():
    return render_template('register.html')

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
    sql2 = 'SELECT Week, Thigh FROM Thigh' 
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    sql3 = 'SELECT Week, Uarm FROM Uarm' 
    cursor.execute(sql3) 
    results3 = cursor.fetchall()
    sql4 = 'SELECT Week, Calve FROM Calve' 
    cursor.execute(sql4)
    results4 = cursor.fetchall()
    cursor = get_db().cursor()
    sqltablebiceps = 'SELECT * FROM Biceps'
    cursor.execute(sqltablebiceps)
    resultstablebiceps = cursor.fetchall()
    sqltablethigh = 'SELECT * FROM Thigh'
    cursor.execute(sqltablethigh)
    resultstablethigh = cursor.fetchall()
    sqltableuarm = 'SELECT * FROM Uarm'
    cursor.execute(sqltableuarm)
    resultstableuarm = cursor.fetchall()
    sqltablecalve = 'SELECT * FROM Calve'
    cursor.execute(sqltablecalve)
    resultstablecalve = cursor.fetchall()
    return render_template('homepage.html', resultstablebiceps=resultstablebiceps, resultstablethigh=resultstablethigh, resultstableuarm=resultstableuarm, resultstablecalve=resultstablecalve, data = [['Date', 'Circumference']] + results, data1 = [['Date', 'Circumference']] + results1 , data2 = [['Date', 'Circumference']] + results2 , data3 = [['Date', 'Circumference']] + results3 , data4 = [['Date', 'Circumference']] + results4 )



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

#add to table(thigh)
@app.route('/add_thigh', methods=['GET','POST'])
def add_thigh():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_thigh = request.form['item_thigh']
        new_week = request.form['item_week']
        if new_thigh.isdigit() & new_week.isdigit():
            sql = 'SELECT Week from Thigh WHERE Week = ?'
            cursor.execute(sql,(new_week,))
            results = cursor.fetchall()
            if len(results) == 0:
                if int(new_week) > 0:
                    cursor = get_db().cursor()
                    sql = 'INSERT INTO Thigh(Week,Thigh) VALUES(?,?)'
                    cursor.execute(sql,(new_week,new_thigh,))
                    get_db().commit()
                    return redirect('/#Tables')  
            if len(results) == 1:
                flash('An error has accured, try again!')
                return redirect('/#Tables') 
        else:
            flash('An error has accured, try again!')
        return redirect('/#Tables') 

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
    return redirect("/#Tables")




#TABLE BICEPS

#add to table biceps
@app.route('/add_biceps', methods=['GET','POST'])
def add_biceps():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_biceps = request.form['item_biceps']
        new_week = request.form['item_week']
        if new_biceps.isdigit() & new_week.isdigit():
            sql = 'SELECT Week from Biceps WHERE Week = ?'
            cursor.execute(sql,(new_week,))
            results = cursor.fetchall()
            if len(results) == 0:
                if int(new_week) > 0:
                    cursor = get_db().cursor()
                    sql = 'INSERT INTO Biceps(Week,Biceps) VALUES(?,?)'
                    cursor.execute(sql,(new_week,new_biceps))
                    get_db().commit()
                return redirect('/#Tables')  
            if len(results) == 1:
                flash('An error has accured, try again!')
            return redirect('/#Tables') 
        else:
            flash('An error has accured, try again!')
        return redirect('/#Tables') 

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
    return redirect('/#Tables')






#TABLE UARM

#add to table uram
@app.route('/add_uarm', methods=['GET','POST'])
def add_uarm():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_uarm = request.form['item_uarm']
        new_week = request.form['item_week']
        if new_uarm.isdigit() & new_week.isdigit():
            sql = 'SELECT Week from Uarm WHERE Week = ?'
            cursor.execute(sql,(new_week,))
            results = cursor.fetchall()
            if len(results) == 0:
                if int(new_week) > 0:
                    cursor = get_db().cursor()
                    sql = 'INSERT INTO Uarm(Week,Uarm) VALUES(?,?)'
                    cursor.execute(sql,(new_week,new_uarm,))
                    get_db().commit()
                    return redirect('/#Tables')  
            if len(results) == 1:
                flash('An error has accured, try again!')
                return redirect('/#Tables') 
        else:
            flash('An error has accured, try again!')
        return redirect('/#Tables') 

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
    return redirect("/#Tables")

#TABLE Calve

#add to calve(calve)
@app.route('/add_calve', methods=['GET','POST'])
def add_calve():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_calve = request.form['item_calve']
        new_week = request.form['item_week']
        if new_calve.isdigit() & new_week.isdigit():
            sql = 'SELECT Week from Calve WHERE Week = ?'
            cursor.execute(sql,(new_week,))
            results = cursor.fetchall()
            if len(results) == 0:
                if int(new_week) > 0:
                    cursor = get_db().cursor()
                    sql = 'INSERT INTO Calve(Week,Calve) VALUES(?,?)'
                    cursor.execute(sql,(new_week,new_calve,))
                    get_db().commit()
                    return redirect('/#Tables')  
            if len(results) == 1:
                flash('An error has accured, try again!')
                return redirect('/#Tables') 
        else:
            flash('An error has accured, try again!')
        return redirect('/#Tables') 

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
    return redirect("/#Tables")


#Register
@app.route('/add_user', methods=['POST'])
def add_user():
    cursor = get_db().cursor()
    username = request.form['item_username']
    password = request.form['item_password']
    password_confirm = request.form['item_password_confirm']
    if hasNumbers(username):
        flash("Username can't have digits")
        return redirect('/login/register')
    else:
        if len(str(username))>1 or len(str(password))>1 or len(str(password_confirm))>1:
            if str(password) == str(password_confirm):
                sql = 'SELECT Username from Users WHERE Username = ?'
                cursor.execute(sql,(username,))
                results = cursor.fetchall()
                print(results)
                if len(results) == 0:
                    if len(str(password)) >= 8:
                        cursor = get_db().cursor()
                        sql = 'INSERT INTO Users(User_ID,Username,Password) VALUES(NULL,?,?)'
                        cursor.execute(sql,(username,password,))    
                        get_db().commit()    
                        return redirect('login/register')    
                    else:
                        flash('Your password needs to be at least 8 digits long')
                        redirect('/login/register')
                else:
                    flash('This Username already exists')
                return redirect('/login/register')
            else:
                flash('Your confirmation of your password was incorrect')
            return redirect('/login/register')
        else:
            flash('Fill all the gaps please!')
        return redirect('/login/register')



@app.route('/loginn', methods=['POST'])
def logging_in():
    cursor = get_db().cursor()
    username = request.form['item_username']
    password = request.form['item_password']
    if hasNumbers(username):
        flash("Username can't have digits")
        return redirect('/login/loginn')
    else:
        sql = 'SELECT Username, Password FROM Users WHERE Username = ? AND Password = ?'
        cursor.execute(sql,(username,password,))
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            flash('Your Username or Password is incorrect')
            return redirect('/login/loginn')
        else:
            
            return redirect('/login/loginn')
    





if __name__== '__main__':
    app.run(debug=True)