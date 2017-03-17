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
    if 'user_id' in session:
        events = []
        upcoming = []
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('getNextThree')
            data = cur.fetchall()

            for datum in data:
                event = {}
                event['id'] = datum[5]
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

        return render_template('home/index.html', event = events, next = upcoming)
    else:
        return redirect('/')    

@app.route('/signup')
def signup():
    if 'user_id' not in session:
        return render_template('signup/index.html')
    else:
        return redirect('/')    

@app.route('/view/event/<event_id>')
def view_event(event_id):
    if 'user_id' in session:

        event_data = {}

        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('checkJoinStatus', [session['user_id'], event_id])
            data = cur.fetchone()
            if data is None:
                event_data['joinStats'] = 0
            else:
                event_data['joinStats'] = 1

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()

        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('viewEvent', [event_id])
            data = cur.fetchone()

            if data is None:
                return render_template('view_event/error.html')
                
            else:
                event_data['id'] = event_id
                event_data['title'] = data[0]
                event_data['desc'] = data[1]
                event_data['date'] = data[2]

                hours, remainder = divmod(data[3].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                starttime = '%02d:%02d' % (hours, minutes)

                event_data['starttime'] = starttime

                hours, remainder = divmod(data[4].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                endtime = '%02d:%02d' % (hours, minutes)

                event_data['endtime'] = endtime
         
                event_data['location'] = data[5]

                return render_template('view_event/index.html', event = event_data)

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()
    else:
        return redirect('/signin')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        info = {}

        # get profile info
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('profileInfo', [session['user_id']])
            data = cur.fetchone()

            profile = {}

            profile['firstName'] = data[0]
            profile['lastName'] = data[1]
            profile['email'] = data[2]
            profile['contactNumber'] = data[3]
            profile['designation'] = data[4]

            info['profile'] = profile

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()

        # get hosted events
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('getUpcomingHostedEvents', [session['user_id']])
            data = cur.fetchall()

            hosted = []

            for item in data:
                event = {}

                event['eventId'] = item[0]
                event['eventName'] = item[1]

                hosted.append(event)

            info['hosted'] = hosted

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()

        # get joined events
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('getUpcomingJoinedEvents', [ session['user_id'] ])
            data = cur.fetchall()

            joined = []

            for item in data:
                print(item)
                event = {}

                event['eventId'] = item[0]
                event['eventName'] = item[1]
                event['eventDate'] = item[2]

                hours, remainder = divmod( item[3].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                event['startTime'] =  '%02d:%02d' % (hours, minutes)

                hours, remainder = divmod(item[4].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                event['endTime'] = '%02d:%02d' % (hours, minutes)
                
                event['venueName'] = item[5]
                event['guestId'] = item[6]

                joined.append(event)

            info['joined'] = joined

        finally:
            cur.close()

        print(info)

        return render_template('profile/index.html', data = info)
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

@app.route('/join/event/<event_id>')
def join(event_id):
    if 'user_id' in session:
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('joinEvent', [session['user_id'], event_id])
            con.commit()
            return render_template('view_event/success.html')

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()
    else:
        return redirect('/signin')

@app.route('/cancel/hosted/<event_id>')
def cancel_hosted(event_id):
    if 'user_id' in session:
        return render_template('/profile/cancelHosted.html', id = event_id)
    else:
        return redirect('/signin')

@app.route('/cancel/hosted/<event_id>/confirm')
def cancel_hosted_confirm(event_id):
    if 'user_id' in session:
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('cancel_hosted', [ event_id ])
            con.commit()

            return redirect('/profile')

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()
    else:
        return redirect('/signin')

@app.route('/cancel/join/<guest_id>')
def cancel_joined(guest_id):
    if 'user_id' in session:
        return render_template('/profile/cancelJoined.html', id = guest_id)
    else:
        return redirect('/signin')

@app.route('/cancel/joined/<guest_id>/confirm')
def cancel_joined_confirm(guest_id):
    if 'user_id' in session:
        try:
            con = mysql.connection
            cur = con.cursor()
            cur.callproc('cancelJoinEvent', [ guest_id ])
            con.commit()

            return redirect('/profile')

        except Exception as e:
            con.rollback()
            return e

        finally:
            cur.close()
    else:
        return redirect('/signin')

########################################################################################################################

#@organizer ############################################################################################################
@app.route('/create/event', methods = ['POST'])
def create_():
    dump = json.dumps(request.form)
    data = json.loads(dump)
    
    print(data)
    venueId = 2
    organizerId = 1

    sql = "SELECT * FROM event a, venue b, venueInfo c WHERE DATE(a.eventDate) = '%s' AND (a.startTime BETWEEN CAST('%s' AS TIME) AND CAST('%s' AS TIME)) AND (a.endTime BETWEEN CAST('%s' AS TIME) AND CAST('%s' AS TIME)) AND a.venueId = '%s' AND (a.status = '%s' OR a.status = '%s') AND a.venueId = b.venueId AND b.venueInfoId = c.venueInfoId AND '%s' <= c.capacity" % \
        (data['date'],data['startTime'],data['endTime'],data['startTime'],data['endTime'],data['venue'],'reserved','published',data['peopleAlloc'])

    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        response = cur.fetchone()

        if response is None:
            sql = "INSERT INTO event (eventName, eventDesc, eventDate, startTime, endTime, venueId, organizerId, peopleAlloc) \
                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                 (data['eventName'], data['eventDesc'], data['date'], data['startTime'], data['endTime'], venueId, organizerId, data['peopleAlloc'])

            con = mysql.connection
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            return redirect('/create/event')
        else:
            return render_template('login/error.html')

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