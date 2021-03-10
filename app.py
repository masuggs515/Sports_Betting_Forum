from flask import Flask, render_template
import requests
import json
from models import db, connect_db, User
from secret import API_KEY


app = Flask(__name__)
app.config["SECRET_KEY"] = 'bettinggnitteb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sports_forum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

res = requests.get(f'https://api.the-odds-api.com/v3/sports/?apiKey={API_KEY}')
json_data = res.json()['data']


@app.route('/')
def home_page():

    sports = retrieve_sport_key(res.json())
    return render_template('home.html', sports=sports)

@app.route('/%7B/all-games/<sport>')
def all_games_in_sport(sport):
    return f"Hi {sport}"




def retrieve_sport_key(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    sports = []

    for sport in json_data:
        key = sport['title']
        sports.append(key)

    return sports

# run = print_json(json_data)
