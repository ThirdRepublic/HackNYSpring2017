from flask import *
from flask_pymongo import PyMongo

app = Flask(__name__) 
app.config.from_object(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def register():
	name = request.form['name']
	phone = request.form['phoneNumber']
	zipcode = request.form['zipcode']
	gmail = request.form['gmail']
	password = request.form['password']
    #store into database
	return render_template('index.html', msg = "You successfully registered. Please log in again.")

@app.route("/dashboard", methods = ['POST'])
def login():
    phoneNum = request.form['phone']
    password = request.form['pw']
    #compare to database, if math, render dashboard, else, return to index
	#pull to check if alarm is being set, if not, then set alarmTime to "not set"
    return render_template('dashboard.html', alarmTime = "insert data from database")
	
@app.route("/dashboard", methods = ['POST'])
def edit():
	alarm = request.form['alarmTime']
	news = request.form['category']
	alarmmsg = ""
	newsmsg = ""
	if alarm is not None: 
		#store alarm data into database
		alarmmsg = "New alarm time has been set!"
	if news is not None: 
		#store news data into database
		newsmsg = "News categories have been set!"
	return render_template('dashboard.html', alarmTime = alarm, alarmMsg = alarmmsg, newsMsg = newsmsg)

if __name__ == "__main__":
    app.run(debug=True)
