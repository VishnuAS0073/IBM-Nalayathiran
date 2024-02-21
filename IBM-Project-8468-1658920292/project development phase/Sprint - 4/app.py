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


# Load the Random Forest CLassifier model
filename = './Model/rainfall.pkl'
clf = pickle.load(open(filename, 'rb'))

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
    return redirect('/Dashboard')


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
            return redirect(url_for('dashboard'))  
    return render_template('login.html')
    

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')
    
@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        min_temp = float(request.form['MinTemp'])
        max_temp = float(request.form['MaxTemp'])
        rainfall = float(request.form['Rainfall'])
        evaporation = float(request.form['Evaporation'])
        sunshine = float(request.form['Sunshine'])
        wind_gust_speed = float(request.form['WindGustSpeed'])
        wind_speed_9am = float(request.form['WindSpeed9am'])
        wind_speed_3pm = float(request.form['WindSpeed3pm'])
        humidity9am = float(request.form['Humidity9am'])
        humidity3pm = float(request.form['Humidity3pm'])
        pressure9am = float(request.form['Pressure9am'])
        pressure3pm = float(request.form['Pressure3pm'])
        cloud9am = float(request.form['Cloud9am'])
        cloud3pm = float(request.form['Cloud3pm'])
        temp9am = float(request.form['Temp9am'])
        temp3pm = float(request.form['Temp3pm'])
        rainToday = request.form['RainToday']
        if rainToday == 'Yes':
            rainToday = 1
        else:
            rainToday = 0
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']

        location = request.form['Location']
        if location == 'Albany':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Albury':
            temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'AliceSprings':
            temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'BadgerysCreek':
            temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Ballarat':
            temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Bendigo':
            temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Brisbane':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Cairns':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Canberra':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Cobar':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'CoffsHarbour	':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Dartmoor':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Darwin':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'GoldCoast':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Hobart':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Katherine':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Launceston':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Melbourne':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'MelbourneAirport':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Mildura':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Moree':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'MountGambier':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'MountGinini':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Newcastle':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Nhil':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'NorahHead':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'NorfolkIsland':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Nuriootpa':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'PearceRAAF':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Penrith':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Perth':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'PerthAirport':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Portland':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Richmond':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Sale':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'SalmonGums':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Sydney':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'SydneyAirport':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Townsville':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Tuggeranong':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'Uluru':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif location == 'WaggaWagga':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif location == 'Walpole':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif location == 'Watsonia':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif location == 'Williamtown':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif location == 'Witchcliffe':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif location == 'Wollongong':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        elif location == 'Woomera':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        else:
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            
        wind_gust_dir = request.form['WindGustDir']
        if wind_gust_dir == 'ENE':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'ESE':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'N':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'NE':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'NNE':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'NNW':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'NW':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'S':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
        elif wind_gust_dir == 'SE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
        elif wind_gust_dir == 'SSE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
        elif wind_gust_dir == 'SSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
        elif wind_gust_dir == 'SW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
        elif wind_gust_dir == 'W':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
        elif wind_gust_dir == 'WNW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
        elif wind_gust_dir == 'WSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
        else :
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
        
        wind_dir_9am = request.form['WindDir9am']
        if wind_dir_9am == 'ENE':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'ESE':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'N':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'NE':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'NNE':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'NNW':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'NW':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'S':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
        elif wind_dir_9am == 'SE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
        elif wind_dir_9am == 'SSE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
        elif wind_dir_9am == 'SSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
        elif wind_dir_9am == 'SW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
        elif wind_dir_9am == 'W':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
        elif wind_dir_9am == 'WNW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
        elif wind_dir_9am == 'WSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
        else :
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


        wind_dir_3pm = request.form['WindDir3pm']
        if wind_dir_3pm == 'ENE':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'ESE':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'N':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'NE':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'NNE':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'NNW':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'NW':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'S':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
        elif wind_dir_3pm == 'SE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
        elif wind_dir_3pm == 'SSE':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
        elif wind_dir_3pm == 'SSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
        elif wind_dir_3pm == 'SW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
        elif wind_dir_3pm == 'W':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
        elif wind_dir_3pm == 'WNW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
        elif wind_dir_3pm == 'WSW':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
        else :
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        
        temp_array = [min_temp, max_temp, rainfall, evaporation, sunshine, wind_gust_speed, wind_speed_9am, wind_speed_3pm, humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, temp9am, temp3pm, rainToday, year, month, day] + temp_array 
        
        data = np.array([temp_array])
        my_prediction = int(clf.predict(data)[0])

              
        return render_template('result.html', my_prediction=my_prediction)

@app.route('/go_back')
def go_back():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)