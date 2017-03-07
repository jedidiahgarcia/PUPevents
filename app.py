from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'startup'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')
    # cur = mysql.connection.cursor()
    # # cur.execute('''SELECT user, host FROM mysql.user''')
    # cur.execute('''SELECT * from registration''')
    # rv = cur.fetchall()
    # return str(rv)

@app.route('/signin')
def signin():
    return render_template('login/index.html')

if __name__ == '__main__':
    app.run(debug=True)