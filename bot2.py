from flask import Flask, request
import requests
import json
import random

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/")
def index():
    url = 'https://thecocktaildb.com/api/json/v1/1/random.php'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        mdata = data["drinks"]
        aname = [item["strDrink"] for item in mdata]
        fname = [aname[0]]
        name = fname
    else:
        name = "I could not retrieve your recipe"
    return str(f'{name[0]}')


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'drink' in incoming_msg:
        url = 'https://thecocktaildb.com/api/json/v1/1/random.php'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            recipe = data["drinks"]
            name = [item["strDrink"] for item in recipe]
            drink = [item["strDrinkThumb"] for item in recipe]
            fname = f'{drink[0]}'
            msg.body(f'{name[0]}')
            msg.media(str(fname))
            responded = True
    if 'mix' in incoming_msg:
        url = 'https://thecocktaildb.com/api/json/v1/1/random.php'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            recipe = data["drinks"]
            name = [item["strDrink"] for item in recipe]
            result = [item["strInstructions"] for item in recipe]
            msg.body(f'{name[0]}: {result[0]}')
            responded = True
    if 'german' in incoming_msg:
        url = 'https://thecocktaildb.com/api/json/v1/1/random.php'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            recipe = data["drinks"]
            name = [item["strDrink"] for item in recipe]
            result = [item["strInstructionsDE"] for item in recipe]
            msg.body(f'{name[0]}: {result[0]}')
            responded = True   
    if 'picture' in incoming_msg:
        msg.media('https://source.unsplash.com/random/400x400')
        responded = True
    if not responded:
        msg.body = "I could not retrieve what you asked from the db"
    return str(resp)


if __name__ == "__main__":
    app.run()
