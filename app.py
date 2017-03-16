from flask import Flask, request, render_template, redirect, jsonify, Response
from flask_mysqldb import MySQL

import json
import hashlib

session = {}

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pupevents'

mysql = MySQL(app)

#@Page rendering and Routes #############################################################################################

@app.route('/')
def default():
    if 'user_id' not in session:

        events = []
        upcoming = []

        
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('getNextThree')
            data = cur.fetchall()

            for datum in data:
                print(datum)
                event = {}
                event['title'] = datum[0]
                event['date'] = datum[1]

                hours, remainder = divmod(datum[2].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                starttime = '%02d:%02d' % (hours, minutes)

                event['starttime'] = starttime

                hours, remainder = divmod(datum[3].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                endtime = '%02d:%02d' % (hours, minutes)

                event['endtime'] = endtime

                event['location'] = datum[4]
                upcoming.append(event)

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()

        #############################################################################################################

        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('getAllEvents')
            data = cur.fetchall()

            for datum in data:
                event = {}

                event['id'] = datum[0]
                event['title'] = datum[1]
                event['startYear'] = datum[2].year
                event['startmonth'] = datum[2].month
                event['startday'] = datum[2].day
                event['starttimehrs'] = datum[3].seconds//3600
                event['starttimemnts'] = (datum[3].seconds//60)%60
                event['endyear'] = datum[2].year
                event['endmonth'] = datum[2].month
                event['endday'] = datum[2].day
                event['endtimehrs'] = datum[4].seconds//3600
                event['endtimemnts'] = (datum[4].seconds//60)%60
                
                events.append(event)

        except Exception as e:
            con.rollback()
            return e
        finally:
            cur.close()

        return render_template('index.html', event = events, next = upcoming)

        ############################################################################################################
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
    dump = json.dumps(request.form)
    data = json.loads(dump)

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

    sql = "SELECT password FROM user where id='%s'" % data['studentNumber']

    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        response = cur.fetchone()

        if response is None:
            sql = "INSERT INTO  USER(id, firstName, lastName, contactNumber, designation, email, password) \
                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (data['studentNumber'], data['firstName'], data['lastName'], data['contactNumber'], data['designation'], data['email'], hashed_pw)

            cur.execute(sql)
            con.commit()
            session['user_id'] = data['studentNumber']
            return redirect('/home')
        else:
            return render_template('signup/error.html',
                                   designation = data['designation'],
                                   studentNumber = data['studentNumber'],
                                   firstName = data['firstName'],
                                   lastName = data['lastName'],
                                   contactNumber = data['contactNumber'],
                                   email = data['email'],
                                   message = "Account already exist")

    finally:
        cur.close()

@app.route('/signin', methods = ['POST'])
def signin_():
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

        if(response is None):
            return render_template('login/error.html',
                identification = data['identification'],
                status = 'Error',
                message = 'Account doesn\'t exist')
        else:
            account_password = response[0];

            if(account_password == hashed_pw):
                session['user_id'] = data['identification']

                return redirect('/home')
            else:
                return render_template('login/error.html',
                    identification=data['identification'],
                    password=data['password'],
                    status='Error',
                    message='Invalid password')

    except Exception as e:
        con.rollback()
        return None

    finally:
        cur.close()

########################################################################################################################

#@organizer ############################################################################################################
@app.route('/create/event', methods = ['POST'])
def create_():
    dump = json.dumps(request.form)
    data = json.loads(dump)
    
    venueId = 9
    organizerId = 9
    reserve = 'reserve'
    
    sql = "INSERT INTO event a, guest b(a.eventName, a.eventDesc, a.date, a.startTime, a.endTime, a.venueId, a.organizerId, a.peopleAlloc, a.status) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
       (data['eventName'], data['eventDesc'], data['date'], data['startTime'], data['endTime'], venueId, organizerId, data['peopleAlloc'], reserve)
    '''
    sql = "INSERT INTO samp(id, name) \
       VALUES ('%d', '%s')" %\
       (venueId, reserve)
    '''
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return redirect('/create/event')

    except TypeError as e:
        mysql.connection.rollback()
        return e

    except Exception as e:
        con.rollback()
        return e

    finally:
        cur.close()
			
########################################################################################################################

def message(type, message):
    data = {
        "type": type,
        "message": message
    }

    response = Response(
        response=json.dumps(data),
        status=200,
        headers={
            'Content-Type': 'application/json'
        }
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)