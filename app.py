from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
import json

from werkzeug import generate_password_hash, check_password_hash
session = {}
session['user_id'] = '2014-05666-MN-0'

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'pupevents'

mysql = MySQL(app)

    # cur.execute('''SELECT user, host FROM mysql.user''')
    # return str(rv)

#@Page rendering and Routes #############################################################################################

@app.route('/')
def default():
    #request the calendar data
    #render calendar with data
    if 'user_id' not in session:
        return render_template('index.html')
    else:
        return redirect('/home')

@app.route('/signin')
def signin():
    return render_template('login/index.html')

@app.route('/create/event')
def create():
    if 'user_id' in session:
        return render_template('create_event/index.html')
    else:
        return redirect('/signin')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home/index.html')
    else:
        return redirect('/')

@app.route('/signup/instructor')
def sign_instructor():
    return render_template('signup_instructor/index.html')

@app.route('/signup/student')
def sign_student():
    return render_template('signup_student/index.html')

@app.route('/view/event')
def view_event():
    return render_template('view_event/index.html')

@app.route('/profile')
def profile():
    # return render_template('view_event/index.html')
    return 'Profile Page Here'

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect('/')

########################################################################################################################

#@form integration######################################################################################################

@app.route('/signup/<designation>', methods = ['POST'])
def sign(designation):
    dump = json.dumps(request.form)
    data = json.loads(dump)

    cur = mysql.connection.cursor()
    
    sql = "INSERT INTO  USER(id, firstName, lastName, contactNumber, designation, email, password) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
       (data['studentNumber'], data['firstName'], data['lastName'], data['contactNumber'], designation, data['email'], data['password'])

    try:
        cur.execute(sql)
        mysql.connection.commit()
        return redirect('/home')
    except Exception as e:
        mysql.connection.rollback()
        return e

@app.route('/signin/', methods = ['POST'])
def signin_():
    if request.method == 'POST':
        #check password first here
        session['user_id'] = request.form['email']
        return redirect('/home')

########################################################################################################################


if __name__ == '__main__':
    app.run(debug=True)