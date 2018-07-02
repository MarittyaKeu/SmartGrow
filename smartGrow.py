from flask import Flask, render_template, request, session
import datetime
import os
from flaskext.mysql import MySQL
import grow_functions as grow

app = Flask(__name__)
mysql = MySQL()

#configure database host, DB name, username, and password
app.config['MYSQL_DATABASE_USER'] = 'mike'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Marittya1'
app.config['MYSQL_DATABASE_DB'] = 'iotdevdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#setting secret key
app.config['SECRET_KEY'] = 'super secret key'


def template(title = 'Hello!', text = ''):
    now = datetime.datetime.now()
    timeString = now;
    templateDate = {
        'title': title,
        'time': timeString,
        'text': text
        }
    return templateDate

#homepage
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'HELLO! welcome back. <a href="/logout">Logout</a>'

#logout function
@app.route('/logout')
def logout():
    session['logged_in'] = False
    grow.led_off()
    return home()

#Authenticate admin username and password	
@app.route('/Authenticate', methods=['POST'])
def Authenticate():
    username = request.form['username']
    password = request.form['password']
    query = str("SELECT * from login where L1='" + username + "' and L2 = md5('" + password + "')")
    cursor = mysql.connect().cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return 'Wrong credentials! <br/><a href="/"><button>Back</button></a>'
    else:
        session['logged_in'] = True
        return render_template('index.html')
 
@app.route('/valve')
def valve():
    grow.activate_valve()
    templateData = template(text = "The valve has been activated")
    return render_template('index.html', **templateData)

@app.route('/soil_reading')
def soil_moist_reading():
    reading =  "The soil moisture level is {}".format(grow.soil_moist_level())
    templateData = template(text = reading)
    if(grow.soil_moist_level() < 200):
        grow.soil_bad()
    else:
        grow.soil_good()
    return render_template('index.html', **templateData)

@app.route('/auto_plant')
def auto():
    reading = ''
                
    if(grow.soil_moist_level() < 200):
        grow.soil_bad()
        grow.send_email('marittyakeu@gmail.com',
                       ['ankimith1@hotmail.com', 'marittya_keu@yahoo.com'],
                       [''],
                       'Warning',
                       'The soil moisture level is low, and we just watered your plant!!!!!\n\nThe SmartGrow Team',
                       'gmail',
                       'password')
        reading = 'soil moisture level is {} and an e-mail was sent to you!'.format(grow.soil_moist_level())
        grow.activate_valve()
        
    else:
        grow.soil_good()
        reading = 'Your plant is in good condition!'
    templateData = template(text = reading)
    return render_template('index.html', **templateData)
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
