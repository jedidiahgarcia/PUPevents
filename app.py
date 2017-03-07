from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'startup'

mysql = MySQL(app)

@app.route('/')
def default():
    return render_template('index.html')
    # cur = mysql.connection.cursor()
    # # cur.execute('''SELECT user, host FROM mysql.user''')
    # cur.execute('''SELECT * from registration''')
    # rv = cur.fetchall()
    # return str(rv)

@app.route('/signin')
def signin():
    return render_template('login/index.html')

@app.route('/create/event')
def create():
    return render_template('create_event/index.html')

@app.route('/home')
def home():
    return render_template('home/index.html')

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
    # return render_template('view_event/index.html')
    return 'Signout action here'

if __name__ == '__main__':
    app.run(debug=True)