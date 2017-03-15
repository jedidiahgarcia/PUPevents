from flask import Flask, request, render_template, redirect, jsonify, Response
from flask_mysqldb import MySQL

import json
import hashlib

session = {}

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = '12345'
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
    if 'user_id' not in session:
        return render_template('login/index.html')
    else:
        return redirect('/home')

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

@app.route('/signup')
def signup():
    if 'user_id' not in session:
        return render_template('signup/index.html')
    else:
        return redirect('/')    

@app.route('/view/event')
def view_event():
    return render_template('view_event/index.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
    # return render_template('view_event/index.html')
        return 'Profile Page Here'
    else:
        return redirect('/')  

@app.route('/signout')
def signout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect('/')

########################################################################################################################

#@form integration######################################################################################################

@app.route('/signup', methods = ['POST'])
def signup_():
    dump = json.dumps(request.form)
    data = json.loads(dump)

    hashed_pw = hashlib.sha256(data['studentNumber'].encode() + data['password'].encode()).hexdigest()
    
    sql = "INSERT INTO  USER(id, firstName, lastName, contactNumber, designation, email, password) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
       (data['studentNumber'], data['firstName'], data['lastName'], data['contactNumber'], data['designation'], data['email'], hashed_pw)

    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        session['user_id'] = data['studentNumber']
        return redirect('/home')

    except Exception as e:
        con.rollback()
        return e

    except TypeError as e:
        mysql.connection.rollback()
        return message('error', 'Identification number already exist.')

    finally:
        cur.close()

@app.route('/signin', methods = ['POST'])
def signin_():
    if request.method == 'POST':
        dump = json.dumps(request.form)
        data = json.loads(dump)
        hashed_pw = hashlib.sha256(data['identification'].encode() + data['password'].encode()).hexdigest()

        sql = "SELECT password FROM user where id='%s'" % data['identification']

        try:
            con = mysql.connection
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            response = cur.fetchone()

            account_password = response[0];

            if(response is None):
                return message('error', "Account doesn't exist")
            else:
                if(account_password == hashed_pw):
                    session['user_id'] = data['identification']
                    return redirect('/home')
                else:
                    return message('error', "Invalid password.")

        except Exception as e:
            con.rollback()
            return None

        except TypeError as e:
            con.rollback()
            return None

        finally:
            cur.close()

########################################################################################################################

def message(type, message):
    data = {
        'type': type,
        'message': message
    }
    return Response(json.dumps(data), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()