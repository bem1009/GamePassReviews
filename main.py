from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class GameData:
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), unique=True, nullable=False)
    #description = db.Column(db.String(120))
    def __init__(self, gameType):
        self.gameType = gameType


    def getGameDataBethesda(self):
        response = requests.get("https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds=BQ1W1T1FC14W,C3KLDKZBHNCZ,"
                               "BS6WJ2L56B10,BRKX5CRMRTC2,9P5S26314HWQ,BX3JNK07Z6QK,BT9FFLG51VVG,C2M8HBNVPT1T,C5K89TFLSV19,"
                               "BSZM480TSWGP,C299QVC2BSJF,BQMVWCMB8P59&market=US&languages=en-us&MS-CV=DGU1mcuYo0WMMp+F.1")

        return json.loads(response.content)


@app.route('/GetGamesList', methods=['GET'])
def getGamePassList():
    response = requests.get("https://catalog.gamepass.com/sigls/v2?id=29a81209-df6f-"
                            "41fd-a528-2ae6b91f719c&language=en-us&market=US")

    data = json.loads(response.content)
    gamesList = []
    for ids in data:
        for key,val in ids.items():
            if key == 'id':
                gamesList.append(val)
    #get games?
    for game in gamesList:
        print(game)

    url = "https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds="

    #append all of the game ids to the API request
    #for game in gamesList:
        #url += game + ","

    for i in range(20):
        url += game + ","

    url = url[:-1]
    url += "&market=US&languages=en-us&MS-CV=DGU1mcuYo0WMMp"

    gameResponse = requests.get(url)

    gameData = json.loads(gameResponse.content)



    return render_template('index.html', data=gameData['Products'])






@app.route('/Games', methods=['GET'])
def printGames():
    games = GameData("Bethesda")
    data = games.getGameDataBethesda()
    products = data["Products"]
    #print(products['LastModifiedDate'])
    for datas in products:
        #print(datas["LocalizedProperties"])
        for names in datas["LocalizedProperties"]:
            print(names['ProductTitle'])


    return render_template('index.html', data=data['Products'])

@app.route('/')
def index():

    return "updated?"
