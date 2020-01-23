from flask import Flask, request
import requests
import json

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/")
def index():
    url = 'https://thecocktaildb.com/api/json/v1/1/random.php'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        recipe = data["drinks"]
        aname = [item["strDrink"] for item in recipe]
        fname = [aname[0]]
        name = fname
    else:
        name = "I could not retrieve your recipe"
    return str(name)


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
            drink = [item["strDrink"] for item in recipe]
            fname = f'{drink}'
            print(fname)
            msg.body(fname)
            responded = True
    if 'picture' in incoming_msg:
        msg.media('https://source.unsplash.com/random/400x400')
        responded = True
    if not responded:
        msg.body = "I could not retrieve a drink from the db"
    return str(resp)


if __name__ == "__main__":
    app.run()
