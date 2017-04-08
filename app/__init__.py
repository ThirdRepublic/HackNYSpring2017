from flask import *

app = Flask(__name__) 
app.config.from_object(__name__)

@app.route("/main.html")
def main():
    return render_template('index.html', data="hello")

if __name__ == "__main__":
    app.run(debug=True)
