# Importing essential libraries
from flask import Flask, render_template, request, url_for, redirect, flash,session,abort
from flask import *
from google_auth_oauthlib.flow import Flow
#from authlib.integration.flask_client import OAuth
import pickle
import catboost as ctp
import numpy as np
import os
import pathlib


app = Flask(__name__)
app.secret_key = "super secret key"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = "734412505534-sjfq66jpvdhnog36hjg3t6fi7mk8qsjr.apps.googleusercontent.com"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_Auth.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/contacts",
    "https://www.google.com/m8/feeds/",
    "https://www.googleapis.com/auth/contacts","openid"],
    redirect_uri="http://127.0.0.1:5000/callbackByGoogle"
    ) #"https://www.googleapis.com/auth/userinfo.profile", "https://www/googleapis.com/auth/userinfo.email",

@app.route("/loginByGoogle")
def loginByGoogle():
   authorization_url, state = flow.authorization_url()
   session["state"] = state
   return redirect(authorization_url)

@app.route("/callbackByGoogle")
def callbackByGoogle():
    flow.fetch_token(authorization_response = request.url)
    if not session["state"] == request.args["state"]:
        abort(500)
    
    credentials = flow.credentials
    request_session = request.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Reauest(sessio = cached_session)

    id_info = id_token.verify_oauth2.token(
        id_token=credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
    )
    session['google_id']= id_info.get('sub')
    session['name']=id_info.det('name')
    return redirect('/Hello')


@app.route('/')
def home():
	return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/req', methods=['POST'])
def req():
    if request.method == 'POST':
        mail = request.form['mailid']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['conpassword']
    return render_template('login.html')

@app.route('/login')
def login():
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
            return redirect(url_for('Hello'))  
    return render_template('login.html')
    

@app.route('/Hello')
def Hello():
    return render_template('hello.html')


if __name__ == '__main__':
	app.run(debug=True)