# Importing essential libraries
from flask import *


app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/req', methods=['POST'])
def req():
    if request.method == 'POST':
        mail = request.form['mailid']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['conpassword']
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    print(request)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        if username != "VishnuAS@0073" or password != "Eizo@0073":
            flash("you are not allowed to logged in")
        else:  
            flash("you are successfuly logged in")  
            return redirect(url_for('hello'))  
    return render_template('login.html')
    

@app.route('/Hello')
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
	app.run(debug=True)