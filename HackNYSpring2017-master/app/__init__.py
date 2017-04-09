from flask import *
from flask_pymongo import PyMongo

app = Flask(__name__) 
app.config.from_object(__name__)

@app.route("/")
def main():
    return render_template('index.html', data="hello")


@app.route("/dashboard", methods = ['POST'])
def my_form_post():
    text = request.form['phone']
    password = request.form['']
    phoneNumber = request["phoneNumber"]
    
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
